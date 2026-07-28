from abc import ABC, abstractmethod

class WeatherService(ABC):
    @abstractmethod
    def get_current_weather(self, lat: float, lon: float):
        """Fetch current weather from API"""
        pass
        
    @abstractmethod
    def get_forecast(self, lat: float, lon: float, days: int):
        """Fetch weather forecast for given days"""
        pass
