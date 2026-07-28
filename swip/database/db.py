import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'predictions.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            rainfall REAL,
            humidity REAL,
            soil_moisture REAL,
            soil_type TEXT,
            crop_type TEXT,
            field_size REAL,
            prediction INTEGER,
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
            timestamp, temperature, rainfall, humidity, soil_moisture, 
            soil_type, crop_type, field_size, prediction, risk_score, water_required
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp, data['temperature'], data['rainfall'], data['humidity'],
        data['soil_moisture'], data['soil_type'], data['crop_type'],
        data['field_size'], data['prediction'], data['risk_score'], data['water_required']
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
