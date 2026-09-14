class WaterCalculator:
    def __init__(self):
        # Base Kc values (mid-season approx)
        self.crop_coefficients = {
            'Cotton': 1.15,
            'Wheat': 1.1,
            'Tomato': 1.15,
            'Potato': 1.15,
            'Onion': 1.05,
            'Cucumber': 1.0
        }
        
        self.stage_multipliers = {
            'Initial': 0.4,
            'Development': 0.8,
            'Mid-Season': 1.0,
            'Late-Season': 0.6
        }

    def calculate_irrigation_requirement(self, et0, rainfall, soil_moisture, field_size_ha, crop_type, growth_stage):
        # 1. Determine Kc
        base_kc = self.crop_coefficients.get(crop_type, 1.0)
        stage_mult = self.stage_multipliers.get(growth_stage, 1.0)
        kc = base_kc * stage_mult
        
        # 2. Crop Evapotranspiration (ETc)
        etc = et0 * kc
        
        # 3. Effective Rainfall (simplistic)
        effective_rain = rainfall * 0.8
        
        # 4. Soil moisture contribution
        # If soil moisture is high, it contributes to meeting the need
        # Assume 1% moisture above wilting point (say 15%) gives 1mm available water
        available_soil_water = max(0, soil_moisture - 15) * 0.5 
        
        # 5. Net Irrigation Requirement (mm)
        net_irrigation_mm = etc - effective_rain - available_soil_water
        net_irrigation_mm = max(0.0, round(net_irrigation_mm, 2))
        
        # 6. Gross volume (Liters)
        # 1 mm over 1 Hectare = 10,000 Liters
        irrigation_efficiency = 0.75 # assume 75% efficiency
        gross_liters = (net_irrigation_mm * 10000 * field_size_ha) / irrigation_efficiency
        
        return {
            "amount_mm": net_irrigation_mm,
            "water_liters": round(gross_liters),
            "priority": "HIGH" if net_irrigation_mm > 10 else "MEDIUM" if net_irrigation_mm > 0 else "LOW"
        }

water_calculator = WaterCalculator()
