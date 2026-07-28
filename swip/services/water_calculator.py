CROP_COEFFICIENTS = {
    'Cotton': 1.3,
    'Wheat': 0.8,
    'Tomato': 1.2,
    'Potato': 1.0,
    'Onion': 0.9,
    'Cucumber': 1.1
}

def calculate_water_requirement(field_size_hectares, crop_type, soil_moisture):
    base_water_per_hectare = 10000 # baseline liters per hectare when dry
    moisture_factor = max(100 - soil_moisture, 0) / 100.0 # higher moisture -> less water
    coef = CROP_COEFFICIENTS.get(crop_type, 1.0)
    
    water_required = field_size_hectares * base_water_per_hectare * moisture_factor * coef
    return {"water_required_liters": round(water_required, 2)}
