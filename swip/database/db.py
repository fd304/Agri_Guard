import json
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB_PATH = Path(os.environ.get('SWIP_DB_PATH', Path(__file__).with_name('predictions.db')))
COLUMNS = {
    'timestamp': 'TEXT', 'location': 'TEXT', 'temperature': 'REAL', 'rainfall': 'REAL',
    'humidity': 'REAL', 'soil_moisture': 'REAL', 'soil_type': 'TEXT', 'crop_type': 'TEXT',
    'field_size': 'REAL', 'prediction': 'INTEGER', 'yield_prediction': 'REAL',
    'risk_score': 'INTEGER', 'water_required': 'REAL', 'growth_stage': 'TEXT',
    'model_version': 'TEXT', 'raw_recommended': 'INTEGER', 'net_irrigation_mm': 'REAL',
    'soil_moisture_source': 'TEXT', 'decision_json': 'TEXT',
}
PERIODS = ('7', '30', '90', 'all')


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH, timeout=10)) as conn, conn:
        conn.execute('CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY AUTOINCREMENT)')
        existing = {row[1] for row in conn.execute('PRAGMA table_info(predictions)')}
        for name, kind in COLUMNS.items():
            if name not in existing:
                conn.execute(f'ALTER TABLE predictions ADD COLUMN {name} {kind}')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON predictions(timestamp)')


def insert_prediction(data):
    record = {key: data.get(key) for key in COLUMNS}
    record['timestamp'] = datetime.now(timezone.utc).isoformat()
    if isinstance(record.get('decision_json'), dict):
        record['decision_json'] = json.dumps(record['decision_json'], allow_nan=False)
    with closing(sqlite3.connect(DB_PATH, timeout=10)) as conn, conn:
        cursor = conn.execute(f"INSERT INTO predictions ({', '.join(COLUMNS)}) VALUES ({', '.join('?' for _ in COLUMNS)})",
                              tuple(record.values()))
        return cursor.lastrowid


def get_recent_predictions(limit=100, period='all', now=None):
    if isinstance(limit, bool) or not 1 <= limit <= 1000 or period not in PERIODS:
        raise ValueError('Invalid history filters')
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('Date boundaries must be timezone aware')
    sql = 'SELECT * FROM predictions'
    parameters = []
    if period != 'all':
        start = now - timedelta(days=int(period))
        sql += ' WHERE julianday(timestamp) >= julianday(?) AND julianday(timestamp) <= julianday(?)'
        parameters = [start.isoformat(), now.isoformat()]
    sql += ' ORDER BY julianday(timestamp) DESC, id DESC LIMIT ?'
    with closing(sqlite3.connect(DB_PATH, timeout=10)) as conn:
        conn.row_factory = sqlite3.Row
        records = [dict(row) for row in conn.execute(sql, (*parameters, limit))]
    for record in records:
        record.pop('decision_json', None)
        record['provenance'] = 'legacy_unverified' if record.get('model_version') is None else 'synthetic_model_user_inputs'
        stamp = record.get('timestamp')
        if stamp:
            try:
                parsed = datetime.fromisoformat(stamp)
                record['timestamp'] = parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).astimezone(timezone.utc).isoformat()
            except ValueError:
                record['timestamp'] = None
    return records


def database_available():
    try:
        with closing(sqlite3.connect(DB_PATH, timeout=2)) as conn:
            conn.execute('SELECT id FROM predictions LIMIT 1').fetchone()
        return True
    except sqlite3.Error:
        return False
