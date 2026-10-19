class SoilService:
    def __init__(self):
        pass

    def estimate_soil_moisture(self, rainfall, temperature, previous_moisture=None):
        """
        If no sensor or manual data is provided, estimate soil moisture based on recent weather.
        """
        if previous_moisture is None:
            # Fallback simplistic estimate
            estimated = 20 + (rainfall * 2) - (temperature * 0.5)
            return max(0.0, min(100.0, round(estimated, 1)))
        
        # Simple decay model
        decay_factor = 0.95 if temperature < 25 else 0.85
        estimated = (previous_moisture * decay_factor) + (rainfall * 2)
        return max(0.0, min(100.0, round(estimated, 1)))

    def process_soil_moisture(self, input_moisture, moisture_source, rainfall, temperature):
        """
        Returns a validated moisture value and its authoritative source label.
        """
        if moisture_source == 'sensor' and input_moisture is not None:
            return {"value": input_moisture, "source": "User-reported sensor value (not independently verified)"}
        elif moisture_source == 'manual' and input_moisture is not None:
            return {"value": input_moisture, "source": "User entered"}
        else:
            est = self.estimate_soil_moisture(rainfall, temperature)
            return {"value": est, "source": "Uncalibrated weather-based heuristic, not measured"}

soil_service = SoilService()
