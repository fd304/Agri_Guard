import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_model():
    data_path = os.path.join(os.path.dirname(__file__), '../data/agricultural_data.csv')
    model_dir = os.path.join(os.path.dirname(__file__), '../models')
    
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run dataset_generator.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Feature engineering / Encoding
    label_encoders = {}
    for col in ['Crop_Type', 'Soil_Type']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Separate features and target
    X = df.drop('Irrigate', axis=1)
    y = df['Irrigate']
    
    # Scale numerical features (Temperature, Rainfall, Humidity, Soil_Moisture, Field_Size)
    # We will just scale everything including encoded categoricals for simplicity, 
    # but normally you'd scale just numerical. Let's do it right.
    scaler = StandardScaler()
    numerical_cols = ['Temperature', 'Rainfall', 'Humidity', 'Soil_Moisture', 'Field_Size']
    X[numerical_cols] = scaler.fit_transform(X[numerical_cols])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    
    print("--- Model Metrics ---")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print("-----------------------")
    
    # Save model and preprocessors
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    joblib.dump(clf, os.path.join(model_dir, 'irrigation_model.pkl'))
    joblib.dump(label_encoders, os.path.join(model_dir, 'label_encoders.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    
    print("Model and preprocessors saved to /models directory.")

if __name__ == "__main__":
    train_model()
