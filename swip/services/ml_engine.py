import os
import joblib
import pandas as pd

class MLEngine:
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(__file__), '../models')
        self.model = None
        self.label_encoders = None
        self.scaler = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            self.model = joblib.load(os.path.join(self.model_dir, 'irrigation_model.pkl'))
            self.label_encoders = joblib.load(os.path.join(self.model_dir, 'label_encoders.pkl'))
            self.scaler = joblib.load(os.path.join(self.model_dir, 'scaler.pkl'))
        except FileNotFoundError:
            print("Model artifacts not found. Please train the model first.")

    def predict(self, temperature, rainfall, humidity, soil_moisture, field_size, crop_type, soil_type):
        if not self.model:
            return 0 # Default to no irrigation if model not loaded
            
        # Encode categorical
        crop_enc = self.label_encoders['Crop_Type'].transform([crop_type])[0]
        soil_enc = self.label_encoders['Soil_Type'].transform([soil_type])[0]

        df = pd.DataFrame({
            'Temperature': [temperature],
            'Rainfall': [rainfall],
            'Humidity': [humidity],
            'Soil_Moisture': [soil_moisture],
            'Field_Size': [field_size],
            'Crop_Type': [crop_enc],
            'Soil_Type': [soil_enc]
        })
        
        # Scale numerical
        numerical_cols = ['Temperature', 'Rainfall', 'Humidity', 'Soil_Moisture', 'Field_Size']
        df[numerical_cols] = self.scaler.transform(df[numerical_cols])

        prediction = self.model.predict(df)[0]
        return int(prediction)

ml_engine = MLEngine()
