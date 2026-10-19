import math


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

    def calculate_irrigation_requirement(self, et0, rainfall, soil_moisture, field_size_ha, crop_type, growth_stage, storage_mm=None):
        values = (et0, rainfall, soil_moisture, field_size_ha)
        if not all(math.isfinite(v) for v in values) or not (0 <= et0 <= 30 and 0 <= rainfall <= 500 and 0 <= soil_moisture <= 100 and 0 < field_size_ha <= 10000):
            raise ValueError('Invalid water-balance inputs')
        if crop_type not in self.crop_coefficients or growth_stage not in self.stage_multipliers:
            raise ValueError('Unsupported crop or growth stage')
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
        # Legacy demonstration proxy, not volumetric moisture or a calibrated soil profile.
        available_soil_water = max(0, soil_moisture - 15) * 0.5 if storage_mm is None else storage_mm
        if not math.isfinite(available_soil_water) or available_soil_water < 0:
            raise ValueError('Invalid initial storage')
        
        # 5. Net Irrigation Requirement (mm)
        net_irrigation_mm = etc - effective_rain - available_soil_water
        net_irrigation_mm = max(0.0, round(net_irrigation_mm, 2))
        
        # 6. Gross volume (Liters)
        # 1 mm over 1 Hectare = 10,000 Liters
        irrigation_efficiency = 0.75 # assume 75% efficiency
        gross_liters = (net_irrigation_mm * 10000 * field_size_ha) / irrigation_efficiency
        
        return {
            "amount_mm": round(net_irrigation_mm, 2),
            "gross_depth_mm": round(net_irrigation_mm / irrigation_efficiency, 2),
            "water_liters": round(gross_liters),
            "water_m3": round(gross_liters / 1000, 3),
            "efficiency": irrigation_efficiency,
            "etc_mm": round(etc, 2),
            "effective_rainfall_mm": round(effective_rain, 2),
            "soil_credit_mm": round(available_soil_water, 2),
            "remaining_storage_mm": max(0.0, available_soil_water + effective_rain - etc),
            "priority": "HIGH" if net_irrigation_mm > 10 else "MEDIUM" if net_irrigation_mm > 0 else "LOW"
        }

    def seven_day_plan(self, forecast, soil_moisture, field_size_ha, crop_type, growth_stage):
        storage = max(0, soil_moisture - 15) * 0.5
        days = []
        for day in forecast:
            balance = self.calculate_irrigation_requirement(day['et0'], day['precipitation'],
                soil_moisture, field_size_ha, crop_type, growth_stage, storage_mm=storage)
            storage = balance.pop('remaining_storage_mm')
            days.append({'date': day['date'], 'rainfall_mm': day['precipitation'],
                         'et0_mm': day['et0'], **balance})
        return {'status': 'available', 'days': days,
                'net_total_mm': round(sum(d['amount_mm'] for d in days), 2),
                'gross_total_liters': sum(d['water_liters'] for d in days),
                'meaning': 'Forecast water-balance scenario, not an irrigation instruction. Initial soil credit applied once; no repeated moisture reset, root-zone calibration or runoff simulation.'}

water_calculator = WaterCalculator()
