class FeatureEngineering:
    def __init__(self):
        pass

    def calculate_et0(self, temperature, humidity, wind_speed=2.0, solar_radiation=15.0):
        """
        Simplified Hargreaves-Samani / Penman-Monteith estimation for ET0.
        Real ET0 requires extensive data. This is an estimate based on available params.
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

    def assess_heat_wave(self, current_temp, forecast_temps):
        """ Check if there's a heatwave in the forecast. """
        consecutive_hot_days = sum(1 for t in forecast_temps if t > 35)
        return current_temp > 35 or consecutive_hot_days >= 3

feature_engineering = FeatureEngineering()
