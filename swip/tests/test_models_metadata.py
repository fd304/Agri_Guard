import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import train_test_split

from models.train import classification_metrics, regression_metrics
from services.data_sources import get_data_sources
from services.ml_engine import MLEngine, ModelUnavailableError, ml_engine
from services.model_contract import FEATURES, CROPS, SOILS, STAGES

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('crop', CROPS)
@pytest.mark.parametrize('stage', STAGES)
@pytest.mark.parametrize('soil', SOILS)
def test_inference_categories_and_feature_contract(crop, stage, soil):
    args = (30, 0, 40, 20, 2, crop, soil, stage)
    irrigation, estimate = ml_engine.predict_irrigation(*args), ml_engine.predict_yield(*args)
    assert isinstance(irrigation['recommended'], bool)
    assert 0 <= irrigation['probability'] <= 100
    assert np.isfinite(estimate['prediction_t_ha'])
    assert 0 <= estimate['range']['lower'] <= estimate['range']['upper']
    assert list(ml_engine.irrigation_pipeline.feature_names_in_) == FEATURES


def test_recorded_metrics_and_train_only_preprocessing_reproduce():
    metadata = json.loads((ROOT / 'models/model_metadata.json').read_text())
    frame = pd.read_csv(ROOT / 'data/agricultural_data.csv')
    train, test = train_test_split(np.arange(len(frame)), test_size=.2, random_state=42, stratify=frame.Irrigate)
    assert len(set(train) & set(test)) == 0
    assert not frame.duplicated(FEATURES).any()
    assert metadata['evaluation']['split']['test_samples'] == len(test) == 400
    assert metadata['evaluation']['split']['test_indices_sha256'] == hashlib.sha256(test.astype('<i8').tobytes()).hexdigest()
    x = frame.iloc[test][FEATURES]
    metrics = metadata['evaluation']['metrics']
    assert classification_metrics(frame.iloc[test].Irrigate, ml_engine.irrigation_pipeline.predict(x),
                                  ml_engine.irrigation_pipeline.predict_proba(x)[:, 1]) == metrics['irrigation_classification']
    assert regression_metrics(frame.iloc[test].Yield_t_ha, ml_engine.yield_pipeline.predict(x)) == metrics['yield_regression']
    expected_mean = frame.iloc[train][FEATURES[:5]].mean().values
    for pipeline in [ml_engine.irrigation_pipeline, ml_engine.yield_pipeline]:
        actual_mean = pipeline.named_steps['preprocessor'].named_transformers_['num'].mean_
        assert np.allclose(actual_mean, expected_mean)


@pytest.mark.parametrize('kind', ['missing', 'malformed', 'version', 'hash', 'corrupt'])
def test_load_failures_are_unavailable(tmp_path, kind):
    metadata = json.loads((ROOT / 'models/model_metadata.json').read_text())
    if kind == 'version':
        metadata['runtime']['scikit_learn'] = 'invalid-version'
    if kind == 'hash':
        metadata['artifacts']['irrigation']['sha256'] = '0' * 64
    if kind == 'corrupt':
        (tmp_path / 'irrigation_model_pipeline.pkl').write_bytes(b'corrupt')
        metadata['artifacts']['irrigation']['sha256'] = hashlib.sha256(b'corrupt').hexdigest()
    if kind != 'missing':
        (tmp_path / 'model_metadata.json').write_text('not json' if kind == 'malformed' else json.dumps(metadata))
    engine = MLEngine(tmp_path)
    assert not engine.available
    with pytest.raises(ModelUnavailableError):
        engine.predict_irrigation(30, 0, 40, 20, 2, 'Cotton', 'Loamy', 'Mid-Season')


def test_invalid_model_output_rejected(monkeypatch):
    class Invalid:
        def predict(self, frame):
            return [1]

        def predict_proba(self, frame):
            return [[0, float('nan')]]
    monkeypatch.setattr(ml_engine, 'irrigation_pipeline', Invalid())
    with pytest.raises(ModelUnavailableError):
        ml_engine.predict_irrigation(30, 0, 40, 20, 2, 'Cotton', 'Loamy', 'Mid-Season')


def test_metadata_normal_missing_and_malformed_stable_schema(tmp_path):
    normal = get_data_sources(model_available=True)
    missing = get_data_sources(tmp_path / 'missing.json')
    malformed_path = tmp_path / 'malformed.json'
    for contents in ['not json', '{}', 'null', '[1,2]', '{"schema_version": NaN}']:
        malformed_path.write_text(contents)
        malformed = get_data_sources(malformed_path)
        assert set(malformed) == set(normal) == set(missing)
        assert malformed['status'] == missing['status'] == 'unavailable'
        assert malformed['model'] is None and malformed['dataset'] is None
        assert str(tmp_path) not in json.dumps(malformed)
    optional_missing = get_data_sources(dataset_path=tmp_path / 'missing.csv', model_available=True)
    assert optional_missing['status'] == 'warning'
    assert optional_missing['dataset']['rows'] == 2000
    assert optional_missing['dataset']['file_integrity_verified'] is False


@pytest.mark.parametrize('fault', ['empty_evaluation', 'wrong_features', 'wrong_split_size', 'nonfinite', 'naive_date'])
def test_metadata_contract_malformed_states(tmp_path, fault):
    raw = json.loads((ROOT / 'models/model_metadata.json').read_text())
    if fault == 'empty_evaluation':
        raw['evaluation'] = {}
    elif fault == 'wrong_features':
        raw['features'] = ['Unknown']
    elif fault == 'wrong_split_size':
        raw['evaluation']['split']['test_samples'] = 1
    elif fault == 'nonfinite':
        raw['evaluation']['metrics']['yield_regression']['r2'] = float('nan')
    else:
        raw['training_date'] = '2026-10-19T10:00:00'
    path = tmp_path / 'metadata.json'
    path.write_text(json.dumps(raw))
    result = get_data_sources(metadata_path=path, model_available=True)
    assert result['status'] == 'unavailable'
    assert result['model'] is result['dataset'] is result['evaluation'] is None
    assert str(tmp_path) not in json.dumps(result)
