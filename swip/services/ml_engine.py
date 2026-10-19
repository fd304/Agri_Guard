import hashlib
import json
import logging
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.exceptions import InconsistentVersionWarning

from .model_contract import FEATURES

logger = logging.getLogger(__name__)


class ModelUnavailableError(RuntimeError):
    pass


class MLEngine:
    def __init__(self, model_dir=None):
        self.model_dir = Path(model_dir or Path(__file__).resolve().parents[1] / 'models')
        self.irrigation_pipeline = self.yield_pipeline = None
        self.model_version = None
        self.load_artifacts()

    @property
    def available(self):
        return self.irrigation_pipeline is not None and self.yield_pipeline is not None

    def load_artifacts(self):
        self.irrigation_pipeline = self.yield_pipeline = None
        try:
            metadata = json.loads((self.model_dir / 'model_metadata.json').read_text())
            if metadata['runtime']['scikit_learn'] != sklearn.__version__ or metadata['features'] != FEATURES:
                raise ValueError('Incompatible model contract')
            loaded = []
            for kind in ('irrigation', 'yield'):
                artifact = metadata['artifacts'][kind]
                filename = f'{kind}_model_pipeline.pkl'
                if artifact['filename'] != filename:
                    raise ValueError('Unexpected artifact name')
                path = self.model_dir / filename
                if hashlib.sha256(path.read_bytes()).hexdigest() != artifact['sha256']:
                    raise ValueError('Artifact integrity check failed')
                # A version warning is a failed load, never a warning to hide.
                with warnings.catch_warnings():
                    warnings.simplefilter('error', InconsistentVersionWarning)
                    pipeline = joblib.load(path)
                if list(pipeline.feature_names_in_) != FEATURES:
                    raise ValueError('Model feature order mismatch')
                loaded.append(pipeline)
            if list(loaded[0].classes_) != [0, 1]:
                raise ValueError('Unexpected irrigation labels')
            self.irrigation_pipeline, self.yield_pipeline = loaded
            self.model_version = metadata['model_version']
        except Exception:
            logger.error('Operational models unavailable: verify packaged artifacts, metadata and pinned dependencies.')

    def _frame(self, values):
        if not self.available:
            raise ModelUnavailableError('Models unavailable. Check artifacts and the documented environment.')
        return pd.DataFrame([values], columns=FEATURES)

    def predict_irrigation(self, *values):
        frame = self._frame(values)
        prediction = self.irrigation_pipeline.predict(frame)[0]
        probability = float(self.irrigation_pipeline.predict_proba(frame)[0][1])
        if prediction not in (0, 1) or not np.isfinite(probability) or not 0 <= probability <= 1:
            raise ModelUnavailableError('Model returned an invalid probability.')
        return {'recommended': bool(prediction == 1), 'probability': round(probability * 100, 1),
                'probability_meaning': 'Uncalibrated forest class score, not probability of field success'}

    def predict_yield(self, *values):
        frame = self._frame(values)
        estimate = float(self.yield_pipeline.predict(frame)[0])
        forest = self.yield_pipeline.named_steps['regressor']
        transformed = self.yield_pipeline.named_steps['preprocessor'].transform(frame)
        tree_predictions = [tree.predict(transformed)[0] for tree in forest.estimators_]
        if not np.isfinite([estimate, *tree_predictions]).all() or estimate < 0:
            raise ModelUnavailableError('Model returned an invalid yield estimate.')
        lower, upper = np.percentile(tree_predictions, [10, 90])
        return {'prediction_t_ha': round(estimate, 2),
                'range': {'lower': round(max(0, lower), 2), 'upper': round(upper, 2)},
                'range_meaning': '10th–90th percentile of trees, not a calibrated prediction interval',
                'validation': 'Synthetic-target holdout only; yield is not guaranteed'}


ml_engine = MLEngine()
