import copy
import math
from datetime import date, datetime, timedelta, timezone

import httpx

LOCATIONS = {
    'dushanbe': {'lat': 38.5598, 'lon': 68.7870, 'name': 'Dushanbe'},
    'khujand': {'lat': 40.2826, 'lon': 69.6222, 'name': 'Khujand'},
    'kulob': {'lat': 37.9146, 'lon': 69.7845, 'name': 'Kulob'},
    'bokhtar': {'lat': 37.8385, 'lon': 68.7770, 'name': 'Bokhtar'},
    'istaravshan': {'lat': 39.9142, 'lon': 69.0033, 'name': 'Istaravshan'},
    'tursunzoda': {'lat': 38.5144, 'lon': 68.2333, 'name': 'Tursunzoda'},
    'panjakent': {'lat': 39.4952, 'lon': 67.6093, 'name': 'Panjakent'},
    'khorugh': {'lat': 37.4922, 'lon': 71.5516, 'name': 'Khorugh'},
    'sughd': {'lat': 40.2826, 'lon': 69.6222, 'name': 'Sughd'},
    'khatlon': {'lat': 37.8385, 'lon': 68.7770, 'name': 'Khatlon'},
    'badakhshan': {'lat': 37.4922, 'lon': 71.5516, 'name': 'Badakhshan'},
    'drs': {'lat': 38.8667, 'lon': 69.5000, 'name': 'Districts of Republican Subordination'},
}


class WeatherUnavailableError(RuntimeError):
    pass


def number(value, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError('Invalid provider measurement')
    return value


class WeatherService:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=30)
        self.max_stale = timedelta(hours=2)

    async def get_locations(self):
        return [{'id': key, **value} for key, value in LOCATIONS.items()]

    def normalize(self, raw, location_id):
        location = LOCATIONS[location_id]
        current, daily = raw['current'], raw['daily']
        fields = ['time', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum',
                  'precipitation_probability_max', 'weather_code', 'et0_fao_evapotranspiration']
        if any(not isinstance(daily[key], list) or len(daily[key]) != 7 for key in fields):
            raise ValueError('Incomplete forecast')
        dates = [date.fromisoformat(item) for item in daily['time']]
        provider_date = datetime.fromisoformat(current['time']).date()
        today = (datetime.now(timezone.utc) + timedelta(hours=5)).date()
        if dates != [today + timedelta(days=i) for i in range(7)] or provider_date != today:
            raise ValueError('Outdated or non-consecutive forecast')
        forecast = []
        for i, day in enumerate(dates):
            maximum = number(daily['temperature_2m_max'][i], -70, 65)
            minimum = number(daily['temperature_2m_min'][i], -70, 65)
            if minimum > maximum:
                raise ValueError('Invalid temperature range')
            forecast.append({'date': day.isoformat(), 'max_temp': maximum, 'min_temp': minimum,
                'precipitation': number(daily['precipitation_sum'][i], 0, 500),
                'precip_prob': number(daily['precipitation_probability_max'][i], 0, 100),
                'weather_code': number(daily['weather_code'][i], 0, 99),
                'et0': number(daily['et0_fao_evapotranspiration'][i], 0, 30)})
        return {'location': f"{location['name']}, Tajikistan", 'location_id': location_id,
            'latitude': location['lat'], 'longitude': location['lon'], 'data_source': 'live',
            'provider': 'Open-Meteo', 'meaning': 'Provider modelled current conditions and daily forecast, not a farm sensor',
            'timezone': 'Asia/Dushanbe', 'stale': False, 'cache_age_seconds': 0,
            'timestamp': datetime.now(timezone.utc).isoformat(), 'provider_time': current['time'],
            'current': {'temperature': number(current['temperature_2m'], -70, 65),
                'humidity': number(current['relative_humidity_2m'], 0, 100),
                'rainfall': number(current['precipitation'], 0, 500),
                'wind_speed': number(current['wind_speed_10m'], 0, 500),
                'pressure': number(current['surface_pressure'], 300, 1100),
                'weather_code': number(current['weather_code'], 0, 99)},
            'daily_rainfall_mm': forecast[0]['precipitation'], 'et0': forecast[0]['et0'],
            'rainfall_meaning': 'Analysis uses daily forecast precipitation, not current-interval precipitation',
            'forecast': forecast}

    def cached_response(self, cached, stale):
        result = copy.deepcopy(cached['data'])
        today = (datetime.now(timezone.utc) + timedelta(hours=5)).date().isoformat()
        stale = stale or result['forecast'][0]['date'] != today
        result.update(data_source='cache', stale=stale,
                      cache_age_seconds=int((datetime.now(timezone.utc) - cached['timestamp']).total_seconds()))
        if stale:
            result['warning'] = 'Provider unavailable; last valid response (at most two hours old). Not used for a new plan.'
        return result

    async def get_weather_for_location(self, location_id):
        if location_id not in LOCATIONS:
            raise ValueError('Unknown location')
        location = LOCATIONS[location_id]
        now = datetime.now(timezone.utc)
        cached = self.cache.get(location_id)
        today = (now + timedelta(hours=5)).date().isoformat()
        if cached and now - cached['timestamp'] < self.cache_ttl and cached['data']['forecast'][0]['date'] == today:
            return self.cached_response(cached, False)
        params = {'latitude': location['lat'], 'longitude': location['lon'],
            'current': 'temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code,et0_fao_evapotranspiration',
            'timezone': 'Asia/Dushanbe', 'forecast_days': 7}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get('https://api.open-meteo.com/v1/forecast', params=params)
                response.raise_for_status()
                normalized = self.normalize(response.json(), location_id)
            self.cache[location_id] = {'timestamp': now, 'data': normalized}
            return normalized
        except (httpx.HTTPError, ValueError, KeyError, TypeError, OverflowError):
            if cached and now - cached['timestamp'] <= self.max_stale:
                return self.cached_response(cached, True)
            raise WeatherUnavailableError('Open-Meteo is unavailable or returned incomplete data; no weather values were substituted.') from None


weather_service = WeatherService()
