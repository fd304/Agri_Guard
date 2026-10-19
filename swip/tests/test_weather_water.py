import asyncio
import copy
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from services.feature_engineering import feature_engineering
from services.water_calculator import water_calculator
from services.weather_service import WeatherService, WeatherUnavailableError


def provider_payload():
    today = (datetime.now(timezone.utc) + timedelta(hours=5)).date()
    return {'current': {'time': f'{today}T12:00', 'temperature_2m': 25, 'relative_humidity_2m': 50,
                       'precipitation': .2, 'surface_pressure': 950, 'wind_speed_10m': 10, 'weather_code': 0},
        'daily': {'time': [(today + timedelta(days=i)).isoformat() for i in range(7)],
            'temperature_2m_max': [30] * 7, 'temperature_2m_min': [15] * 7, 'precipitation_sum': [2] * 7,
            'precipitation_probability_max': [10] * 7, 'weather_code': [0] * 7,
            'et0_fao_evapotranspiration': [5] * 7}}


def test_weather_validation_daily_rain_is_not_current_interval():
    result = WeatherService().normalize(provider_payload(), 'dushanbe')
    assert len(result['forecast']) == 7
    assert result['current']['rainfall'] == .2 and result['daily_rainfall_mm'] == 2
    assert result['stale'] is False


@pytest.mark.parametrize('key,bad', [('temperature_2m_max', [None] * 7), ('precipitation_sum', [-1] * 7),
    ('precipitation_probability_max', [101] * 7), ('et0_fao_evapotranspiration', [float('nan')] * 7),
    ('time', ['2020-01-01'] * 7), ('temperature_2m_min', [50] * 7), ('weather_code', [])])
def test_incomplete_weather_rejected(key, bad):
    raw = provider_payload()
    raw['daily'][key] = bad
    with pytest.raises(ValueError):
        WeatherService().normalize(raw, 'dushanbe')


def test_weather_fetch_cache_stale_and_failure(monkeypatch):
    service = WeatherService()
    calls = []

    async def fake_get(self, url, params):
        calls.append(params)
        return httpx.Response(200, json=provider_payload(), request=httpx.Request('GET', url))

    monkeypatch.setattr(httpx.AsyncClient, 'get', fake_get)
    live = asyncio.run(service.get_weather_for_location('dushanbe'))
    assert live['data_source'] == 'live'
    cached = asyncio.run(service.get_weather_for_location('dushanbe'))
    assert cached['data_source'] == 'cache' and len(calls) == 1
    assert calls[0]['timezone'] == 'Asia/Dushanbe'
    cached['current']['temperature'] = 99
    assert service.cache['dushanbe']['data']['current']['temperature'] == 25

    async def fail(self, url, params):
        raise httpx.ConnectError('private internal error')

    monkeypatch.setattr(httpx.AsyncClient, 'get', fail)
    service.cache['dushanbe']['timestamp'] -= timedelta(minutes=31)
    stale = asyncio.run(service.get_weather_for_location('dushanbe'))
    assert stale['stale'] and stale['data_source'] == 'cache'
    service.cache['dushanbe']['timestamp'] -= timedelta(hours=2)
    with pytest.raises(WeatherUnavailableError) as error:
        asyncio.run(service.get_weather_for_location('dushanbe'))
    assert 'private' not in str(error.value)
    with pytest.raises(ValueError):
        asyncio.run(service.get_weather_for_location('unknown'))


def test_water_units_efficiency_once_and_initial_credit_once():
    balance = water_calculator.calculate_irrigation_requirement(10, 0, 15, 2, 'Cucumber', 'Mid-Season')
    assert balance['amount_mm'] == 10
    assert balance['water_liters'] == round(10 * 10000 * 2 / .75)
    assert balance['water_m3'] == pytest.approx(balance['water_liters'] / 1000, abs=.001)
    forecast = [{'date': f'2026-10-{i:02}', 'et0': 10, 'precipitation': 0} for i in range(1, 8)]
    plan = water_calculator.seven_day_plan(forecast, 35, 2, 'Cucumber', 'Mid-Season')
    assert plan['days'][0]['amount_mm'] == 0  # 10 mm initial credit only on day 1.
    assert [day['amount_mm'] for day in plan['days'][1:]] == [10] * 6
    assert plan['net_total_mm'] == 60
    assert plan['gross_total_liters'] == round(10 * 10000 * 2 / .75) * 6


def test_cached_forecast_crossing_local_midnight_is_not_used_for_a_new_plan(monkeypatch):
    service = WeatherService()
    data = service.normalize(provider_payload(), 'dushanbe')
    data['forecast'][0]['date'] = '2020-01-01'
    service.cache['dushanbe'] = {'timestamp': datetime.now(timezone.utc), 'data': data}
    calls = []

    async def fail(self, url, params):
        calls.append(url)
        raise httpx.ConnectError('unavailable')

    monkeypatch.setattr(httpx.AsyncClient, 'get', fail)
    result = asyncio.run(service.get_weather_for_location('dushanbe'))
    assert calls and result['stale'] is True
    assert result['data_source'] == 'cache'


@pytest.mark.parametrize('values', [(float('nan'), 0, 10, 2), (5, -1, 10, 2), (5, 0, 101, 2),
    (5, 0, 10, 0), (float('inf'), 0, 10, 2)])
def test_invalid_water_inputs(values):
    with pytest.raises(ValueError):
        water_calculator.calculate_irrigation_requirement(*values, 'Cotton', 'Mid-Season')


def test_heatwave_requires_consecutive_dates_and_not_total_hot_days():
    days = [{'date': f'2026-10-{i:02}', 'max_temp': t} for i, t in enumerate([36, 30, 36, 30, 36], start=1)]
    assert feature_engineering.assess_heat_wave(days) is False
    assert feature_engineering.assess_heat_wave([{'date': f'2026-10-{i:02}', 'max_temp': 36} for i in (1, 2, 4)]) is False
    assert feature_engineering.assess_heat_wave([{'date': f'2026-10-{i:02}', 'max_temp': 36} for i in (1, 2, 3)]) is True


def test_authoritative_plan_and_unavailable_stale_forecast(client, request_data, monkeypatch):
    from services.weather_service import weather_service
    payload = WeatherService().normalize(provider_payload(), 'dushanbe')

    async def forecast(location):
        return copy.deepcopy(payload)

    monkeypatch.setattr(weather_service, 'get_weather_for_location', forecast)
    data = {**request_data, 'weather_location': 'dushanbe'}
    result = client.post('/api/decision', json=data).json()
    assert result['plan']['status'] == 'available' and len(result['plan']['days']) == 7
    payload['stale'] = True
    assert client.post('/api/decision', json=data).json()['plan']['status'] == 'unavailable'
