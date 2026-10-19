import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import database.db as db
from services.report_service import safe_cell


def test_initialization_migration_and_repeat(tmp_path, monkeypatch):
    path = tmp_path / 'existing.db'
    with sqlite3.connect(path) as conn:
        conn.execute('CREATE TABLE predictions (id INTEGER PRIMARY KEY, timestamp TEXT, location TEXT)')
        conn.execute("INSERT INTO predictions VALUES (1, '2026-01-01T00:00:00', 'existing farm')")
    monkeypatch.setattr(db, 'DB_PATH', path)
    db.init_db()
    db.init_db()
    records = db.get_recent_predictions()
    assert len(records) == 1 and records[0]['location'] == 'existing farm'
    assert records[0]['provenance'] == 'legacy_unverified'
    assert records[0]['timestamp'] == '2026-01-01T00:00:00+00:00'
    assert set(db.COLUMNS) <= set(records[0]) | {'decision_json'}


def test_committed_database_preserved_migration(tmp_path, monkeypatch):
    original = Path(__file__).resolve().parents[1] / 'database/predictions.db'
    copy = tmp_path / 'copy.db'
    before = original.read_bytes()
    copy.write_bytes(before)
    monkeypatch.setattr(db, 'DB_PATH', copy)
    with sqlite3.connect(copy) as conn:
        count_before = conn.execute('SELECT count(*) FROM predictions').fetchone()[0]
    db.init_db()
    db.init_db()
    assert len(db.get_recent_predictions()) == count_before == 36
    assert original.read_bytes() == before


@pytest.mark.parametrize('period,days', [('7', 7), ('30', 30), ('90', 90)])
def test_period_boundaries_filters_before_limit(tmp_path, monkeypatch, period, days):
    monkeypatch.setattr(db, 'DB_PATH', tmp_path / 'period.db')
    db.init_db()
    now = datetime(2026, 10, 19, 10, tzinfo=timezone.utc)
    stamps = [now, now - timedelta(days=days), now - timedelta(days=days, seconds=1), now + timedelta(seconds=1)]
    with sqlite3.connect(db.DB_PATH) as conn:
        for stamp in stamps:
            conn.execute('INSERT INTO predictions(timestamp,location) VALUES (?, ?)', (stamp.isoformat(), 'test'))
    assert len(db.get_recent_predictions(100, period, now)) == 2
    assert len(db.get_recent_predictions(1, period, now)) == 1
    assert len(db.get_recent_predictions(100, 'all', now)) == 4


@pytest.mark.parametrize('value', ['=1+1', '+cmd', '-formula', '@SUM(A1)', '\t=cmd', '\r=cmd', '\n=cmd', '  =cmd'])
def test_csv_formula_escaping(value):
    assert safe_cell(value) == "'" + value
    assert safe_cell(-12) == -12
    assert safe_cell('normal') == 'normal'
