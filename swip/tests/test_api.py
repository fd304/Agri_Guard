import csv
import io
import json
import math

import pytest

import database.db as db
from services.ml_engine import ml_engine


def test_health_root_sources_and_security(client):
    assert client.get('/').status_code == 200
    health = client.get('/api/health')
    assert health.status_code == 200
    assert health.json()['models'] == 'available'
    assert health.headers['x-content-type-options'] == 'nosniff'
    source = client.get('/api/data-sources').json()
    assert source['status'] == 'available'
    assert source['dataset']['rows'] == 2000
    assert source['dataset']['observed_farm_outcomes_available'] is False
    assert not any(ref['used_by_operational_dataset'] for ref in source['reference_sources'])
    assert len(client.get('/api/locations').json()) == 12


@pytest.mark.parametrize('route', ['/api/decision', '/api/predict'])
def test_complete_prediction_persisted(client, request_data, route):
    response = client.post(route, json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data['decision']['state'] == 'IRRIGATE'
    assert data['model_irrigation']['recommended']
    assert 0 <= data['model_irrigation']['probability'] <= 100
    assert data['irrigation']['water_liters'] > 0
    assert math.isfinite(data['yield']['prediction_t_ha']) and data['yield']['prediction_t_ha'] > 0
    assert data['plan']['status'] == 'unavailable'
    records = client.get('/api/history').json()['history']
    assert len(records) == 1 and records[0]['id'] == data['history_id']
    assert records[0]['soil_moisture'] == 10
    assert records[0]['prediction'] == 1
    assert records[0]['model_version'] == ml_engine.model_version
    assert records[0]['timestamp'].endswith('+00:00')


@pytest.mark.parametrize('changes,override', [({'soil_moisture': 81}, 'waterlogging'),
    ({'rainfall': 31}, 'heavy_rain'), ({'soil_moisture': 100, 'rainfall': 500}, 'waterlogging')])
def test_safety_overrides_raw_positive_model(client, request_data, monkeypatch, changes, override):
    monkeypatch.setattr(ml_engine, 'predict_irrigation', lambda *args: {'recommended': True, 'probability': 99})
    response = client.post('/api/decision', json={**request_data, **changes})
    assert response.status_code == 200
    data = response.json()
    assert data['model_irrigation']['recommended'] is True
    assert data['decision']['safety_override'] == override
    assert data['decision']['state'] == 'DO_NOT_IRRIGATE'
    assert data['irrigation']['recommended'] is False
    assert data['irrigation']['water_liters'] == data['irrigation']['amount_mm'] == 0
    record = client.get('/api/history').json()['history'][0]
    assert record['prediction'] == 0 and record['raw_recommended'] == 1
    if override == 'waterlogging':
        assert data['risk']['waterlogging'] > 0 and data['risk']['water_stress'] == 0


@pytest.mark.parametrize('field,value', [('temperature', -31), ('temperature', 61), ('rainfall', -1),
    ('rainfall', 501), ('humidity', 101), ('humidity', -1), ('soil_moisture', -1), ('soil_moisture', 101),
    ('field_size', 0), ('field_size', -1), ('field_size', 10001), ('crop_type', 'Unknown'),
    ('soil_type', 'Unknown'), ('growth_stage', 'Unknown'), ('soil_moisture_source', 'unknown'),
    ('language', 'unknown'), ('weather_location', 'unknown'), ('et0_mm', -1), ('et0_mm', 31),
    ('location', ''), ('location', 'x' * 121), ('temperature', 'NaN'), ('humidity', 'Infinity'),
    ('temperature', True), ('rainfall', False), ('field_size', '2')])
def test_invalid_inputs_not_stored(client, request_data, field, value):
    response = client.post('/api/decision', json={**request_data, field: value})
    assert response.status_code == 422
    assert client.get('/api/history').json()['history'] == []


def test_missing_and_nonfinite_json(client, request_data):
    assert client.post('/api/decision', json={}).status_code == 422
    assert client.post('/api/decision', content=json.dumps({**request_data, 'temperature': float('nan')}),
                       headers={'content-type': 'application/json'}).status_code == 422
    assert client.post('/api/decision', json={**request_data, 'soil_moisture': None}).status_code == 422
    estimated = client.post('/api/decision', json={**request_data, 'soil_moisture': None, 'soil_moisture_source': 'estimated'})
    assert estimated.status_code == 200
    assert 'heuristic' in estimated.json()['soil_status']['source']


def test_models_unavailable_fail_closed(client, request_data, monkeypatch):
    monkeypatch.setattr(ml_engine, 'yield_pipeline', None)
    assert client.get('/api/health').status_code == 503
    response = client.post('/api/decision', json=request_data)
    assert response.status_code == 503
    assert client.get('/api/history').json()['history'] == []
    assert 'Traceback' not in response.text


def test_weather_errors_visible_no_fallback(client):
    assert client.get('/api/weather?location=unknown').status_code == 422
    response = client.get('/api/weather?location=dushanbe')
    assert response.status_code == 503
    assert 'current' not in response.json()


@pytest.mark.parametrize('report_type', ['full', 'water', 'yield', 'risk', 'irrigation'])
@pytest.mark.parametrize('period', ['7', '30', '90', 'all'])
def test_report_types_and_periods_empty(client, report_type, period):
    response = client.get('/api/report', params={'report_type': report_type, 'period': period})
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/csv')
    assert response.headers['x-report-record-count'] == '0'
    rows = list(csv.reader(io.StringIO(response.content.decode('utf-8-sig'))))
    assert len(rows) == 1 and rows[0][0] == 'Timestamp (UTC)'


def test_real_csv_data_limit_and_formula_protection(client, request_data):
    for i in range(2):
        assert client.post('/api/decision', json={**request_data, 'location': '=HYPERLINK("invalid")'}).status_code == 200
    response = client.get('/api/report?report_type=yield&period=7&limit=1')
    rows = list(csv.reader(io.StringIO(response.content.decode('utf-8-sig'))))
    assert len(rows) == 2
    assert 'Synthetic-model yield (t/ha)' in rows[0]
    assert rows[1][1].startswith("'=")
    assert response.headers['x-report-record-count'] == '1'


@pytest.mark.parametrize('query', ['report_type=invalid', 'period=season', 'format=pdf', 'limit=0', 'limit=1001', 'limit=-1'])
def test_report_invalid_filters(client, query):
    assert client.get('/api/report?' + query).status_code == 422


def test_database_unavailable_safe_errors(client, request_data, monkeypatch, tmp_path):
    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'missing' / 'db.sqlite')
    assert client.get('/api/health').status_code == 503
    for response in [client.get('/api/history'), client.get('/api/report'), client.post('/api/decision', json=request_data)]:
        assert response.status_code == 503
        assert str(tmp_path) not in response.text


def test_forecast_failure_does_not_fake_plan(client, request_data):
    response = client.post('/api/decision', json={**request_data, 'weather_location': 'dushanbe'})
    assert response.status_code == 200
    assert response.json()['plan']['status'] == 'unavailable'
