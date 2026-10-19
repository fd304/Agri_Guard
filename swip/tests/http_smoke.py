"""Actual HTTP verification. Use only an isolated database; --allow-write adds two scenarios."""
import argparse
import csv
import io
import json
import math
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def smoke(base_url, allow_write=False):
    results = []

    def request(path, expected=200, payload=None):
        body = json.dumps(payload).encode() if payload is not None else None
        req = Request(base_url.rstrip('/') + path, data=body,
                      headers={'Content-Type': 'application/json'} if body else {})
        try:
            response = urlopen(req, timeout=30)
        except HTTPError as error:
            response = error
        with response:
            content = response.read()
            assert response.status == expected, (path, response.status, content[:200])
            assert response.headers['x-content-type-options'] == 'nosniff'
            results.append({'path': path, 'status': response.status})
            return content, response.headers

    def get_json(path, **kwargs):
        return json.loads(request(path, **kwargs)[0])

    assert b'Smart Water Intelligence Platform' in request('/')[0]
    for asset in ['/static/js/app.js', '/static/js/preferences.js', '/static/js/charts.js',
                  '/static/vendor/lucide.js', '/static/css/style.css', '/static/favicon.svg']:
        request(asset)
    health = get_json('/api/health')
    assert health['models'] == health['database'] == 'available'
    source = get_json('/api/data-sources')
    assert source['status'] == 'available' and source['dataset']['rows'] == 2000
    assert not source['dataset']['observed_farm_outcomes_available']
    assert source['dataset']['file_integrity_verified']
    assert len(get_json('/api/locations')) == 12
    # Provider availability is not a prerequisite for truthful manual analysis.
    req = Request(base_url.rstrip('/') + '/api/weather?location=dushanbe')
    try:
        with urlopen(req, timeout=30) as response:
            weather = json.load(response)
            assert weather['data_source'] in ('live', 'cache')
            assert len(weather['forecast']) == 7
            weather_result = {'status': 'available', 'source': weather['data_source'], 'stale': weather['stale']}
    except HTTPError as error:
        assert error.code == 503
        assert 'current' not in json.load(error)
        weather_result = {'status': 'unavailable', 'http_status': 503}
    request('/api/weather?location=unknown', expected=422)
    request('/api/report?format=pdf', expected=422)
    get_json('/api/decision', expected=422, payload={})
    history_before = get_json('/api/history?limit=1000')['history']
    if allow_write:
        scenario = {'location': '=declared hypothetical HTTP test', 'temperature': 40, 'rainfall': 0,
                    'humidity': 20, 'soil_moisture': 10, 'soil_moisture_source': 'manual',
                    'field_size': 2, 'crop_type': 'Cotton', 'soil_type': 'Loamy', 'growth_stage': 'Mid-Season'}
        normal = get_json('/api/decision', payload=scenario)
        assert normal['decision']['state'] == 'IRRIGATE'
        assert normal['irrigation']['water_liters'] > 0
        assert math.isfinite(normal['yield']['prediction_t_ha']) and normal['yield']['prediction_t_ha'] > 0
        assert normal['plan']['status'] == 'unavailable' and normal['plan']['days'] == []
        blocked = get_json('/api/predict', payload={**scenario, 'soil_moisture': 90})
        assert blocked['decision']['state'] == 'DO_NOT_IRRIGATE'
        assert blocked['decision']['safety_override'] == 'waterlogging'
        assert blocked['irrigation']['water_liters'] == blocked['irrigation']['amount_mm'] == 0
        records = get_json('/api/history?limit=1000')['history']
        assert len(records) == len(history_before) + 2
        assert {row['id'] for row in records[:2]} == {normal['history_id'], blocked['history_id']}
        assert records[0]['timestamp'].endswith('+00:00')
        for report_type in ('full', 'water', 'irrigation', 'risk', 'yield'):
            for period in ('7', '30', '90', 'all'):
                content, headers = request(f'/api/report?format=csv&report_type={report_type}&period={period}&limit=1')
                assert content.startswith(b'\xef\xbb\xbf')
                rows = list(csv.reader(io.StringIO(content.decode('utf-8-sig'))))
                assert len(rows) == 2 and rows[0][0] == 'Timestamp (UTC)'
                assert rows[1][1].startswith("'=")
                assert headers['x-report-record-count'] == '1'
    return {'http_checks': results, 'weather': weather_result, 'write_scenarios': 2 if allow_write else 0,
            'model_version': health['model_version'], 'result': 'passed'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8000')
    parser.add_argument('--allow-write', action='store_true', help='Use ONLY against isolated disposable history')
    args = parser.parse_args()
    print(json.dumps(smoke(args.base_url, args.allow_write), indent=2))
