import pandas as pd
import numpy as np
import os
import joblib
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_absolute_error, root_mean_squared_error, r2_score

def train_model():
    data_path = os.path.join(os.path.dirname(__file__), '../data/agricultural_data.csv')
    model_dir = os.path.join(os.path.dirname(__file__), '../models')
    
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run dataset_generator.py first.")
        return

    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Define features and targets
    numerical_features = ['Temperature', 'Rainfall', 'Humidity', 'Soil_Moisture', 'Field_Size']
    categorical_features = ['Crop_Type', 'Soil_Type', 'Growth_Stage']
    
    X = df[numerical_features + categorical_features]
    y_class = df['Irrigate']
    y_reg = df['Yield_t_ha']
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])
    
    # ==========================================
    # 1. IRRIGATION CLASSIFICATION MODEL
    # ==========================================
    print("\n--- Training Irrigation Classifier ---")
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_class, test_size=0.2, random_state=42)
    
    clf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42))
    ])
    
    clf_pipeline.fit(X_train_c, y_train_c)
    y_pred_c = clf_pipeline.predict(X_test_c)
    
    class_metrics = {
        'accuracy': float(accuracy_score(y_test_c, y_pred_c)),
        'precision': float(precision_score(y_test_c, y_pred_c)),
        'recall': float(recall_score(y_test_c, y_pred_c)),
        'f1': float(f1_score(y_test_c, y_pred_c))
    }
    
    print(f"Accuracy:  {class_metrics['accuracy']:.4f}")
    print(f"Precision: {class_metrics['precision']:.4f}")
    print(f"Recall:    {class_metrics['recall']:.4f}")
    print(f"F1 Score:  {class_metrics['f1']:.4f}")
    
    # ==========================================
    # 2. YIELD REGRESSION MODEL
    # ==========================================
    print("\n--- Training Yield Regressor ---")
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    
    reg_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42))
    ])
    
    reg_pipeline.fit(X_train_r, y_train_r)
    y_pred_r = reg_pipeline.predict(X_test_r)
    
    reg_metrics = {
        'mae': float(mean_absolute_error(y_test_r, y_pred_r)),
        'rmse': float(root_mean_squared_error(y_test_r, y_pred_r)),
        'r2': float(r2_score(y_test_r, y_pred_r))
    }
    
    print(f"MAE:  {reg_metrics['mae']:.4f} t/ha")
    print(f"RMSE: {reg_metrics['rmse']:.4f} t/ha")
    print(f"R²:   {reg_metrics['r2']:.4f}")

    # ==========================================
    # 3. SAVING ARTIFACTS
    # ==========================================
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    print("\nSaving models and metadata...")
    joblib.dump(clf_pipeline, os.path.join(model_dir, 'irrigation_model_pipeline.pkl'))
    joblib.dump(reg_pipeline, os.path.join(model_dir, 'yield_model_pipeline.pkl'))
    
    metadata = {
        "training_date": datetime.now().isoformat(),
        "model_version": "2.0",
        "features": numerical_features + categorical_features,
        "metrics": {
            "irrigation_classification": class_metrics,
            "yield_regression": reg_metrics
        }
    }
    
    with open(os.path.join(model_dir, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("All artifacts saved successfully to /models directory.")

if __name__ == "__main__":
    train_model()
