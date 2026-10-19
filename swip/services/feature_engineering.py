class FeatureEngineering:
    def __init__(self):
        pass

    def calculate_et0(self, temperature, humidity, wind_speed=2.0, solar_radiation=15.0):
        """
        Legacy temperature/humidity heuristic (mm/day), not Hargreaves-Samani
        or FAO Penman-Monteith. Defaults for wind/radiation are assumptions.
        """
        # Simplistic approximation: higher temp = higher ET0, higher humidity = lower ET0
        # Base ET0 around 3-6 mm/day for typical summer days
        et0 = (temperature * 0.2) + (solar_radiation * 0.1) - (humidity * 0.05) + (wind_speed * 0.1)
        return max(1.0, round(et0, 2))

    def calculate_water_deficit(self, et0, rainfall, soil_moisture_percentage):
        """
        Calculate water deficit in mm.
        Assuming top 30cm of soil, 1% moisture roughly equals some mm of water.
        For simplicity, Deficit = ET0 - Effective Rainfall
        """
        effective_rainfall = rainfall * 0.8 # Assume 20% runoff/loss
        deficit = et0 - effective_rainfall
        return max(0.0, round(deficit, 2))

    def assess_heat_wave(self, forecast):
        """Three consecutive dated daily maxima >35°C (legacy demo threshold)."""
        from datetime import date, timedelta
        streak, previous = 0, None
        for day in sorted(forecast, key=lambda item: item['date']):
            current = date.fromisoformat(day['date'])
            if current == previous:
                raise ValueError('Duplicate forecast date')
            if previous is None or current != previous + timedelta(days=1):
                streak = 0
            streak = streak + 1 if day['max_temp'] > 35 else 0
            if streak >= 3:
                return True
            previous = current
        return False

feature_engineering = FeatureEngineering()
