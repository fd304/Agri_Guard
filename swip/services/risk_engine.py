class RiskEngine:
    def __init__(self):
        pass

    def calculate_risks(self, soil_moisture, temperature, rainfall, crop_type, growth_stage, yield_range):
        # Base Sub-risks (0-100)
        
        # 1. Drought Risk
        # High when rainfall is low and temperature is high
        drought = max(0, min(100, 100 - (rainfall * 2) + (temperature - 25) * 2))
        
        # 2. Heat Stress Risk
        # High when temperature exceeds 32
        heat_stress = 0
        if temperature > 38: heat_stress = 95
        elif temperature > 32: heat_stress = 60 + (temperature - 32) * 5
        elif temperature > 28: heat_stress = 30
        
        # 3. Water Stress Risk
        # Crop specific
        water_stress = 0
        if soil_moisture < 20: water_stress = 90
        elif soil_moisture < 40: water_stress = 50
        elif soil_moisture > 80: water_stress = 70 # Waterlogging
        
        # 4. Flood / Heavy Rain Risk
        flood = 0
        if rainfall > 50: flood = 80
        elif rainfall > 30: flood = 40
        
        # 5. Yield Risk
        # Derived from yield uncertainty or sub-risks
        yield_spread = yield_range["upper"] - yield_range["lower"]
        yield_risk = min(100, max(0, (yield_spread * 10) + (drought * 0.3) + (heat_stress * 0.3)))
        
        # Overall Risk (Weighted average)
        overall = (drought * 0.3) + (heat_stress * 0.2) + (water_stress * 0.3) + (flood * 0.1) + (yield_risk * 0.1)
        overall = round(overall)
        
        level = "LOW"
        if overall > 70: level = "HIGH"
        elif overall > 35: level = "MEDIUM"
        
        return {
            "overall": overall,
            "level": level,
            "drought": round(drought),
            "heat": round(heat_stress),
            "water_stress": round(water_stress),
            "flood": round(flood),
            "yield_risk": round(yield_risk)
        }

risk_engine = RiskEngine()
