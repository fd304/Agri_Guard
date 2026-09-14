import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'predictions.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Expanded schema to handle new capabilities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            location TEXT,
            temperature REAL,
            rainfall REAL,
            humidity REAL,
            soil_moisture REAL,
            soil_type TEXT,
            crop_type TEXT,
            field_size REAL,
            prediction INTEGER,
            yield_prediction REAL,
            risk_score INTEGER,
            water_required REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_prediction(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO predictions (
            timestamp, location, temperature, rainfall, humidity, soil_moisture, 
            soil_type, crop_type, field_size, prediction, yield_prediction, risk_score, water_required
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp, 
        data.get('location', 'Unknown'),
        data.get('temperature', 0.0), 
        data.get('rainfall', 0.0), 
        data.get('humidity', 0.0),
        data.get('soil_moisture', 0.0), 
        data.get('soil_type', ''), 
        data.get('crop_type', ''),
        data.get('field_size', 0.0), 
        data.get('prediction', 0), 
        data.get('yield_prediction', 0.0),
        data.get('risk_score', 0), 
        data.get('water_required', 0.0)
    ))
    conn.commit()
    conn.close()

def get_recent_predictions(limit=100):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

