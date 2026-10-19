import pytest
from fastapi.testclient import TestClient

import database.db as db
from main import app
from services.weather_service import WeatherUnavailableError, weather_service


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'history.db')

    async def unavailable(location):
        raise WeatherUnavailableError('Weather unavailable in isolated test')

    monkeypatch.setattr(weather_service, 'get_weather_for_location', unavailable)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def request_data():
    return {'location': 'Dushanbe', 'temperature': 40, 'rainfall': 0, 'humidity': 20,
            'soil_moisture': 10, 'field_size': 2, 'crop_type': 'Cotton', 'soil_type': 'Loamy',
            'growth_stage': 'Mid-Season', 'soil_moisture_source': 'manual'}
