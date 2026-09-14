import pandas as pd
import numpy as np
import os

# ==========================================
# WARNING: DEMO DATASET GENERATOR
# This script generates synthetic data for 
# development and demonstration purposes.
# It should not be used as authoritative 
# agronomic truth.
# ==========================================

def generate_synthetic_data(num_samples=2000):
    np.random.seed(42)
    
    # Input ranges
    temperature = np.random.uniform(15, 45, num_samples) # Celsius
    rainfall = np.random.uniform(0, 100, num_samples)    # mm
    humidity = np.random.uniform(20, 90, num_samples)    # %
    soil_moisture = np.random.uniform(10, 80, num_samples) # %
    field_size = np.random.uniform(1, 50, num_samples)   # Hectares
    
    # Categorical
    crop_types = ['Cotton', 'Wheat', 'Tomato', 'Potato', 'Onion', 'Cucumber']
    soil_types = ['Sandy', 'Loamy', 'Clay']
    growth_stages = ['Initial', 'Development', 'Mid-Season', 'Late-Season']
    
    crop = np.random.choice(crop_types, num_samples)
    soil = np.random.choice(soil_types, num_samples)
    stage = np.random.choice(growth_stages, num_samples)
    
    # Target variable generation (Heuristics)
    irrigate = []
    yield_t_ha = []
    
    for i in range(num_samples):
        # 1. Irrigation Classification Logic
        # More sensitive in Mid-Season
        moisture_threshold = 30
        if stage[i] == 'Mid-Season':
            moisture_threshold = 40
            
        if soil_moisture[i] < moisture_threshold:
            irrigate.append(1)
        elif temperature[i] > 35 and rainfall[i] < 10 and soil_moisture[i] < (moisture_threshold + 10):
            irrigate.append(1)
        elif crop[i] in ['Tomato', 'Cucumber'] and soil_moisture[i] < 50:
            irrigate.append(1)
        elif soil[i] == 'Sandy' and soil_moisture[i] < 45:
            irrigate.append(1)
        else:
            irrigate.append(0)
            
        # 2. Yield Regression Logic (Synthetic Demo Yield in ton/ha)
        # Base yield depends on crop
        base_yield = {'Cotton': 2.5, 'Wheat': 3.0, 'Tomato': 40.0, 'Potato': 30.0, 'Onion': 25.0, 'Cucumber': 20.0}[crop[i]]
        
        # Modify by weather/soil conditions
        yield_mod = 1.0
        if temperature[i] > 35: yield_mod -= 0.2  # Heat stress
        if temperature[i] < 18: yield_mod -= 0.1  # Cold stress
        if soil_moisture[i] < 20: yield_mod -= 0.3 # Drought stress
        if soil_moisture[i] > 70: yield_mod -= 0.1 # Waterlogging
        
        # Sandy soil might have lower yield naturally unless perfectly managed
        if soil[i] == 'Sandy': yield_mod -= 0.05
        if soil[i] == 'Loamy': yield_mod += 0.1
        
        # Add some noise
        noise = np.random.normal(0, 0.1)
        
        final_yield = base_yield * yield_mod * (1 + noise)
        final_yield = max(0.5, round(final_yield, 2)) # Minimum yield bounds
        yield_t_ha.append(final_yield)
            
    df = pd.DataFrame({
        'Temperature': temperature,
        'Rainfall': rainfall,
        'Humidity': humidity,
        'Soil_Moisture': soil_moisture,
        'Field_Size': field_size,
        'Crop_Type': crop,
        'Soil_Type': soil,
        'Growth_Stage': stage,
        'Irrigate': irrigate,
        'Yield_t_ha': yield_t_ha
    })
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(2000)
    output_path = os.path.join(os.path.dirname(__file__), 'agricultural_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Demo dataset generated at: {output_path}")
