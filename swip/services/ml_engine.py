import os
import joblib
import pandas as pd
import numpy as np

class MLEngine:
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(__file__), '../models')
        self.irrigation_pipeline = None
        self.yield_pipeline = None
        self.load_artifacts()

    def load_artifacts(self):
        try:
            self.irrigation_pipeline = joblib.load(os.path.join(self.model_dir, 'irrigation_model_pipeline.pkl'))
            self.yield_pipeline = joblib.load(os.path.join(self.model_dir, 'yield_model_pipeline.pkl'))
        except FileNotFoundError:
            print("Model artifacts not found. Please train the model first.")

    def predict_irrigation(self, temperature, rainfall, humidity, soil_moisture, field_size, crop_type, soil_type, growth_stage):
        if not self.irrigation_pipeline:
            return {"recommended": False, "probability": 0.0, "error": "Model not loaded"}
            
        df = pd.DataFrame({
            'Temperature': [temperature],
            'Rainfall': [rainfall],
            'Humidity': [humidity],
            'Soil_Moisture': [soil_moisture],
            'Field_Size': [field_size],
            'Crop_Type': [crop_type],
            'Soil_Type': [soil_type],
            'Growth_Stage': [growth_stage]
        })
        
        prediction = self.irrigation_pipeline.predict(df)[0]
        # Get probability of class 1 (Irrigate)
        probability = self.irrigation_pipeline.predict_proba(df)[0][1]
        
        return {
            "recommended": bool(prediction == 1),
            "probability": round(float(probability * 100), 1) # percentage
        }

    def predict_yield(self, temperature, rainfall, humidity, soil_moisture, field_size, crop_type, soil_type, growth_stage):
        if not self.yield_pipeline:
            return {"prediction_t_ha": 0.0, "range": {"lower": 0.0, "upper": 0.0}, "error": "Model not loaded"}
            
        df = pd.DataFrame({
            'Temperature': [temperature],
            'Rainfall': [rainfall],
            'Humidity': [humidity],
            'Soil_Moisture': [soil_moisture],
            'Field_Size': [field_size],
            'Crop_Type': [crop_type],
            'Soil_Type': [soil_type],
            'Growth_Stage': [growth_stage]
        })
        
        pred_yield = float(self.yield_pipeline.predict(df)[0])
        
        # Estimate uncertainty using standard deviation of trees in the forest
        # Note: pipeline.named_steps['regressor'] gets the RF model
        rf = self.yield_pipeline.named_steps['regressor']
        preprocessor = self.yield_pipeline.named_steps['preprocessor']
        
        X_transformed = preprocessor.transform(df)
        preds = [tree.predict(X_transformed)[0] for tree in rf.estimators_]
        std_dev = np.std(preds)
        
        lower_bound = max(0.0, pred_yield - (1.96 * std_dev))
        upper_bound = pred_yield + (1.96 * std_dev)
        
        return {
            "prediction_t_ha": round(pred_yield, 2),
            "range": {
                "lower": round(lower_bound, 2),
                "upper": round(upper_bound, 2)
            }
        }

ml_engine = MLEngine()
