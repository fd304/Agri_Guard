import httpx
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Predefined locations for Tajikistan, including regions requested by user
LOCATIONS = {
    "dushanbe": {"lat": 38.5598, "lon": 68.7870, "name": "Dushanbe"},
    "khujand": {"lat": 40.2826, "lon": 69.6222, "name": "Khujand"},
    "kulob": {"lat": 37.9146, "lon": 69.7845, "name": "Kulob"},
    "bokhtar": {"lat": 37.8385, "lon": 68.7770, "name": "Bokhtar"},
    "istaravshan": {"lat": 39.9142, "lon": 69.0033, "name": "Istaravshan"},
    "tursunzoda": {"lat": 38.5144, "lon": 68.2333, "name": "Tursunzoda"},
    "panjakent": {"lat": 39.4952, "lon": 67.6093, "name": "Panjakent"},
    "khorugh": {"lat": 37.4922, "lon": 71.5516, "name": "Khorugh"},
    
    # Regions
    "sughd": {"lat": 40.2826, "lon": 69.6222, "name": "Sughd"},
    "khatlon": {"lat": 37.8385, "lon": 68.7770, "name": "Khatlon"},
    "badakhshan": {"lat": 37.4922, "lon": 71.5516, "name": "Badakhshan"},
    "drs": {"lat": 38.8667, "lon": 69.5000, "name": "Districts of Republican Subordination"}
}

class WeatherService:
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = timedelta(minutes=30)
        self.client = httpx.AsyncClient(timeout=10.0)
        
    async def get_locations(self) -> List[Dict[str, Any]]:
        """Return available predefined locations."""
        return [{"id": k, **v} for k, v in LOCATIONS.items()]
        
    async def get_weather_for_location(self, location_id: str) -> Dict[str, Any]:
        """Fetch current weather, forecast, and ET0 for a location."""
        location = LOCATIONS.get(location_id)
        if not location:
            # Default to Dushanbe if not found
            location = LOCATIONS["dushanbe"]
            location_id = "dushanbe"
            
        lat = location["lat"]
        lon = location["lon"]
        
        cache_key = f"{lat}_{lon}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data["timestamp"] < self.cache_ttl:
                data = cached_data["data"].copy()
                data["data_source"] = "cache"
                return data
                
        # Fetch from Open-Meteo
        try:
            # We fetch current weather, hourly for ET0, and daily for forecast
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,et0_fao_evapotranspiration",
                "timezone": "auto"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Normalize the data
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            # Extract today's ET0
            et0_today = daily.get("et0_fao_evapotranspiration", [5.0])[0] if daily.get("et0_fao_evapotranspiration") else 5.0
            
            normalized_weather = {
                "location": f"{location['name']}, Tajikistan",
                "location_id": location_id,
                "latitude": lat,
                "longitude": lon,
                "data_source": "live",
                "current": {
                    "temperature": current.get("temperature_2m", 25),
                    "humidity": current.get("relative_humidity_2m", 50),
                    "rainfall": current.get("precipitation", 0),
                    "wind_speed": current.get("wind_speed_10m", 10),
                    "pressure": current.get("surface_pressure", 1012),
                    "weather_code": current.get("weather_code", 0)
                },
                "et0": et0_today,
                "forecast": [],
                "timestamp": datetime.now().isoformat()
            }
            
            # Build 7-day forecast
            if daily.get("time"):
                for i in range(min(7, len(daily["time"]))):
                    normalized_weather["forecast"].append({
                        "date": daily["time"][i],
                        "max_temp": daily["temperature_2m_max"][i],
                        "min_temp": daily["temperature_2m_min"][i],
                        "precipitation": daily["precipitation_sum"][i],
                        "precip_prob": daily["precipitation_probability_max"][i],
                        "weather_code": daily["weather_code"][i],
                        "et0": daily["et0_fao_evapotranspiration"][i]
                    })
            
            # Update cache
            self.cache[cache_key] = {
                "timestamp": datetime.now(),
                "data": normalized_weather
            }
            
            return normalized_weather
            
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            # Graceful fallback to cached or dummy data
            if cache_key in self.cache:
                data = self.cache[cache_key]["data"].copy()
                data["data_source"] = "cache"
                return data
                
            # Dummy fallback if API completely fails and no cache
            return self._get_fallback_weather(location)
            
    def _get_fallback_weather(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Provides dummy fallback weather if API completely fails."""
        return {
            "location": f"{location['name']}, Tajikistan",
            "location_id": location.get("name", "").lower(),
            "latitude": location["lat"],
            "longitude": location["lon"],
            "data_source": "fallback",
            "current": {
                "temperature": 28,
                "humidity": 45,
                "rainfall": 0,
                "wind_speed": 12,
                "pressure": 1012,
                "weather_code": 0
            },
            "et0": 5.2,
            "forecast": [],
            "timestamp": datetime.now().isoformat(),
            "is_fallback": True
        }

weather_service = WeatherService()
