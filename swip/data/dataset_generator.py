import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=1000):
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
    
    crop = np.random.choice(crop_types, num_samples)
    soil = np.random.choice(soil_types, num_samples)
    
    # Target variable generation (Heuristics)
    irrigate = []
    for i in range(num_samples):
        # Base condition: very low moisture or high temp/low rain combo
        if soil_moisture[i] < 30:
            irrigate.append(1)
        elif temperature[i] > 35 and rainfall[i] < 10 and soil_moisture[i] < 45:
            irrigate.append(1)
        # Specific crop needs (e.g., tomatoes and cucumbers need more water)
        elif crop[i] in ['Tomato', 'Cucumber'] and soil_moisture[i] < 50:
            irrigate.append(1)
        # Sandy soil drains fast
        elif soil[i] == 'Sandy' and soil_moisture[i] < 40:
            irrigate.append(1)
        else:
            irrigate.append(0)
            
    df = pd.DataFrame({
        'Temperature': temperature,
        'Rainfall': rainfall,
        'Humidity': humidity,
        'Soil_Moisture': soil_moisture,
        'Field_Size': field_size,
        'Crop_Type': crop,
        'Soil_Type': soil,
        'Irrigate': irrigate
    })
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(2000)
    output_path = os.path.join(os.path.dirname(__file__), 'agricultural_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at: {output_path}")
