import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, ValidationError

from .model_contract import FEATURES

ROOT = Path(__file__).resolve().parents[1]


class DatasetMetadata(BaseModel):
    name: str
    version: str
    rows: int = Field(ge=1)
    sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    static: Literal[True]
    inputs: str
    soil_moisture: str
    targets: dict[str, str]
    observed_farm_outcomes_available: Literal[False]
    sources: list[dict[str, str]]


class RuntimeMetadata(BaseModel):
    python: str
    scikit_learn: str
    numpy: str
    pandas: str
    joblib: str


class SplitMetadata(BaseModel):
    random_state: int
    test_fraction: float = Field(gt=0, lt=1)
    stratify: str
    train_samples: int = Field(gt=0)
    test_samples: int = Field(gt=0)
    test_indices_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')


class EvaluationMetadata(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    kind: str
    split: SplitMetadata
    preprocessing: str
    duplicate_feature_rows: int = Field(ge=0)
    metrics: dict[str, dict[str, float]]
    baselines_same_split: dict[str, dict[str, float]]
    limitations: str


class OperationalMetadata(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    schema_version: Literal['1.0']
    model_version: str
    training_date: AwareDatetime
    features: list[str]
    runtime: RuntimeMetadata
    dataset: DatasetMetadata
    evaluation: EvaluationMetadata
    uncertainty: str


def get_data_sources(metadata_path=None, dataset_path=None, model_available=False):
    metadata_path = Path(metadata_path or ROOT / 'models/model_metadata.json')
    dataset_path = Path(dataset_path or ROOT / 'data/agricultural_data.csv')
    result = {
        'schema_version': '1.0', 'status': 'unavailable', 'model_available': model_available,
        'model': None, 'dataset': None, 'evaluation': None,
        'live_weather': {'provider': 'Open-Meteo', 'role': 'Operational modelled weather and forecasts, not training data',
                         'availability': 'Request /api/weather for current availability',
                         'url': 'https://open-meteo.com/en/docs'},
        'reference_sources': [
            {'name': 'NASA POWER', 'used_by_operational_dataset': False,
             'meaning': 'Reanalysis/reference data, not individual farm measurements. No imported records found in this repository.'},
            {'name': 'FAOSTAT', 'used_by_operational_dataset': False,
             'meaning': 'National/regional reference statistics. No imported records found in this repository.'}],
        'warnings': [],
    }
    try:
        raw = json.loads(metadata_path.read_text(encoding='utf-8'),
                         parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Non-finite metadata')))
        metadata = OperationalMetadata.model_validate(raw)
        if metadata.features != FEATURES or metadata.evaluation.split.train_samples + metadata.evaluation.split.test_samples != metadata.dataset.rows:
            raise ValueError('Inconsistent training contract')
        values = metadata.model_dump(mode='json')
        result.update(status='available', dataset=values.pop('dataset'), evaluation=values.pop('evaluation'), model=values)
        try:
            verified = hashlib.sha256(dataset_path.read_bytes()).hexdigest() == metadata.dataset.sha256
        except OSError:
            verified = False
        result['dataset']['file_integrity_verified'] = verified
        if not verified:
            result['status'] = 'warning'
            result['warnings'].append('Training CSV unavailable or changed; dataset facts describe the training snapshot, not a verified current file.')
        result['warnings'].append('All training inputs/targets are synthetic; no observed farm outcomes or field validation are available.')
    except (OSError, ValueError, TypeError, ValidationError):
        result['warnings'].append('Operational metadata unavailable or malformed. No substitute source counts or metrics supplied.')
    if not model_available:
        result['warnings'].append('Operational inference is unavailable; see /api/health.')
    return result
