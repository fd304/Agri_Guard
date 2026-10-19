"""Reproducible demonstration pipelines; no observed farm outcomes are available."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, mean_absolute_error, mean_squared_error, r2_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from services.model_contract import NUMERIC_FEATURES, CATEGORICAL_FEATURES, FEATURES

ROOT = Path(__file__).resolve().parents[1]


def classification_metrics(target, predicted, probability):
    return {name: float(value) for name, value in {
        'accuracy': accuracy_score(target, predicted),
        'precision': precision_score(target, predicted, zero_division=0),
        'recall': recall_score(target, predicted, zero_division=0),
        'f1': f1_score(target, predicted, zero_division=0),
        'roc_auc': roc_auc_score(target, probability),
    }.items()}


def regression_metrics(target, predicted):
    return {'mae_t_ha': float(mean_absolute_error(target, predicted)),
            'rmse_t_ha': float(np.sqrt(mean_squared_error(target, predicted))),
            'r2': float(r2_score(target, predicted))}


def make_preprocessor():
    return ColumnTransformer([
        ('num', StandardScaler(), NUMERIC_FEATURES),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES),
    ])


def train_model(data_path=ROOT / 'data/agricultural_data.csv', model_dir=ROOT / 'models', replace=False):
    model_dir, data_path = Path(model_dir), Path(data_path)
    artifacts = {'irrigation': 'irrigation_model_pipeline.pkl', 'yield': 'yield_model_pipeline.pkl'}
    if not replace and any((model_dir / name).exists() for name in artifacts.values()):
        raise FileExistsError('Pipelines already exist; use --replace only after backing them up.')
    frame = pd.read_csv(data_path)
    if frame.isna().any().any() or frame.duplicated(FEATURES).any():
        raise ValueError('Resolve missing values or duplicate feature records before splitting.')
    if not np.isfinite(frame.select_dtypes('number')).all().all():
        raise ValueError('Non-finite training values')
    train_idx, test_idx = train_test_split(
        np.arange(len(frame)), test_size=0.2, random_state=42, stratify=frame['Irrigate'])
    x_train, x_test = frame.iloc[train_idx][FEATURES], frame.iloc[test_idx][FEATURES]
    class_train, class_test = frame.iloc[train_idx]['Irrigate'], frame.iloc[test_idx]['Irrigate']
    yield_train, yield_test = frame.iloc[train_idx]['Yield_t_ha'], frame.iloc[test_idx]['Yield_t_ha']
    classifier = Pipeline([('preprocessor', make_preprocessor()),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42))])
    regressor = Pipeline([('preprocessor', make_preprocessor()),
        ('regressor', RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42))])
    classifier.fit(x_train, class_train)
    regressor.fit(x_train, yield_train)
    dummy_class = DummyClassifier(strategy='most_frequent').fit(x_train, class_train)
    dummy_yield = DummyRegressor(strategy='mean').fit(x_train, yield_train)
    metrics = {
        'irrigation_classification': classification_metrics(
            class_test, classifier.predict(x_test), classifier.predict_proba(x_test)[:, 1]),
        'yield_regression': regression_metrics(yield_test, regressor.predict(x_test))}
    baseline = {
        'irrigation_most_frequent': classification_metrics(
            class_test, dummy_class.predict(x_test), dummy_class.predict_proba(x_test)[:, 1]),
        'yield_training_mean': regression_metrics(yield_test, dummy_yield.predict(x_test))}
    model_dir.mkdir(parents=True, exist_ok=True)
    for name, model in [('irrigation', classifier), ('yield', regressor)]:
        joblib.dump(model, model_dir / artifacts[name], compress=3)
    metadata_path = model_dir / 'model_metadata.json'
    previous = json.loads(metadata_path.read_text()) if metadata_path.exists() else None
    metadata = {
        'schema_version': '1.0', 'model_version': '2.1-synthetic-demo',
        'training_date': datetime.now(timezone.utc).isoformat(),
        'runtime': {'python': platform.python_version(), 'scikit_learn': sklearn.__version__,
                    'numpy': np.__version__, 'pandas': pd.__version__, 'joblib': joblib.__version__},
        'features': FEATURES,
        'artifacts': {name: {'filename': filename,
                            'sha256': hashlib.sha256((model_dir / filename).read_bytes()).hexdigest()}
                      for name, filename in artifacts.items()},
        'dataset': {
            'name': 'SWIP synthetic demonstration dataset', 'version': 'generator-seed-42',
            'rows': len(frame), 'sha256': hashlib.sha256(data_path.read_bytes()).hexdigest(),
            'static': True, 'inputs': 'Synthetic random samples, not observed weather or farm records',
            'soil_moisture': 'Synthetic random percentage, not a measured soil-water profile',
            'targets': {'irrigation': 'Rules in data/dataset_generator.py',
                        'yield': 'Crop-specific heuristic with seeded Gaussian noise'},
            'observed_farm_outcomes_available': False,
            'sources': [{'name': 'SWIP dataset_generator.py', 'kind': 'synthetic_generator'}]},
        'evaluation': {
            'kind': 'generated-target holdout, not field validation',
            'split': {'random_state': 42, 'test_fraction': 0.2, 'stratify': 'Irrigate',
                      'train_samples': len(train_idx), 'test_samples': len(test_idx),
                      'test_indices_sha256': hashlib.sha256(test_idx.astype('<i8').tobytes()).hexdigest()},
            'preprocessing': 'Independent preprocessors fit only on training rows',
            'duplicate_feature_rows': 0, 'metrics': metrics, 'baselines_same_split': baseline,
            'limitations': 'Scores measure reproduction of generated targets, not accuracy on Tajikistan farms.'},
        'uncertainty': 'Yield range is 10th–90th percentile of tree predictions, not a calibrated interval.'}
    if previous:
        metadata['superseded_metadata'] = previous.get('superseded_metadata', previous)
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'metrics': metrics, 'baselines_same_split': baseline}, indent=2))
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replace', action='store_true')
    train_model(replace=parser.parse_args().replace)
