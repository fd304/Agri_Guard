# SWIP — Smart Water Intelligence Platform

**AI-powered agricultural risk and water-management demonstration for Tajikistan.**

FastAPI/Jinja2 + static JavaScript, SQLite history, scikit-learn pipelines, Open-Meteo weather. The existing Tajikistan-focused interface is preserved. This is **not field-validated agronomic guidance** or a calibrated physical simulation. A working demonstration is not evidence of safe agricultural deployment.

## What the repository actually contains

The operational training CSV has 2,000 entirely **synthetic** input/target records from `swip/data/dataset_generator.py` (seed 42). Irrigation targets are rules; yield targets are crop-specific heuristics plus noise. Soil-moisture percentages are synthetic, not a measured soil profile. No imported NASA POWER, FAOSTAT, farm sensor or independently observed farm-outcome records were found. NASA POWER would be reanalysis/reference data and FAOSTAT would be regional/national statistics, not farm observations; neither is claimed as operational training provenance here.

Open-Meteo supplies **modelled current weather and forecasts**, separately from training data. Unknown locations are rejected. Provider failures return an honest unavailable state, never invented weather. Valid responses are cached in server memory for 30 minutes. When the provider fails, a previously validated response at most two hours old can be displayed, explicitly marked stale with age and retrieval time; stale forecasts are not used for new plans. No API key is required. Only configured coordinates are sent to the weather provider; analysis/history is not uploaded to it.

## Windows startup (PowerShell)

Install Python **3.11** (training/verification used **3.11.15**), Git, and optionally Node.js for frontend unit/syntax checks. From the repository root:

```powershell
cd swip
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 on **your own computer**. No activation script is necessary. Startup initializes or additively migrates history; no manual initialization or retraining is required. Existing SQLite records are retained, and legacy records are marked unverified. Before updating an existing installation, stop it and back up `swip/database/predictions.db` (and any SQLite journal files) outside Git. Never reset or delete history to resolve a startup problem.

To use a different history file, set this **before starting**:

```powershell
$env:SWIP_DB_PATH = Join-Path $PWD 'runtime\predictions.db'
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

A new path starts an empty database, not a silently copied history. To relocate existing history, stop the app and copy your backed-up SQLite file to that path first. Keep real farm data out of Git. The committed database is retained byte-for-byte during development verification; tests use separate temporary databases.

Linux/macOS equivalent (Python 3.11):

```sh
cd swip
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## Reproducibility and model compatibility

Runtime dependencies and their resolved closure are pinned in `swip/requirements.lock`; direct dependencies are in `swip/requirements.txt`. Operational scikit-learn is **1.7.2**, not the old 1.3.2 pin or the 1.9.0 version embedded in unused legacy artifacts. Dependencies were deliberately updated for security/compatibility; unused multipart/dotenv dependencies were removed. Do not upgrade sklearn independently of the pipelines. Never load untrusted pickle/joblib files.

The original loader required two pipeline files which were absent. The original training script did not import under its requirements. Both pipelines were deliberately restored by reproducible training, **not merely to hide serialization warnings**. The old classifier/encoder/scaler artifacts are preserved but are not loaded or included in the runtime image. Operational files are explicitly included in Git and Docker.

The authoritative provenance/evaluation record is `swip/models/model_metadata.json`, including artifact/CSV SHA-256 digests, exact runtime versions, feature order, split description, generated-target limitations and superseded historical metadata. Artifact hashes, runtime compatibility and feature order are checked before loading. Missing, corrupt or incompatible models yield health/analysis HTTP 503 and no prediction is stored. Health is not an assertion that the external weather provider is reachable.

Training uses one seeded, irrigation-stratified 80/20 split (1,600 train / **400 test**). Each model has its own preprocessing fitted **only on training rows**. No feature duplicates or train/test overlap were found. Numeric features are scaled; categoricals are one-hot encoded inside each pipeline. Both targets and any derived predictions are excluded from the inputs. Same-split baselines are majority-class irrigation and training-mean yield.

Verified generated-target holdout metrics (not real-farm accuracy):

| Task | Metrics | Same-split baseline |
|---|---|---|
| Irrigation | accuracy 0.9800, precision 0.9841, recall 0.9738, F1 0.9789, ROC-AUC 0.9989 | accuracy 0.5225, F1 0, ROC-AUC 0.5 |
| Yield | MAE 1.5816 t/ha, RMSE 2.5812 t/ha, R² 0.9581 | MAE 10.5834, RMSE 12.6154 t/ha, R² −0.0008 |

These high scores primarily demonstrate learning the generator. They are not independently validated yield estimates or demonstrated irrigation benefit. The classifier score is uncalibrated; it is not a probability of field success. Yield ranges are the 10th–90th percentiles of tree outputs, **not calibrated confidence/prediction intervals** or yield guarantees. Do not compare these numbers to unrelated splits or older metadata as measured improvements.

To retrain deliberately (back up operational artifacts and metadata first):

```powershell
cd swip  # omit if already here
.\.venv\Scripts\python.exe -m models.train --replace
```

Without `--replace`, existing pipelines cannot be overwritten. The CSV is not regenerated or changed by training. Changing the dataset requires a new provenance review: the current trainer explicitly describes this synthetic generator and must not be used to relabel real data automatically.

## Decision and water conventions

- Inputs: daily rainfall **mm/day**, ET0 **mm/day**, area **ha**, moisture **% proxy**, temperature **°C**. Negative rain/area, unsupported categories, nonfinite and out-of-bound inputs are rejected, not silently clamped.
- ETc = ET0 × legacy crop coefficient × stage multiplier. If daily ET0 is not supplied, a labelled temperature/humidity heuristic is used. It is **not** Hargreaves-Samani or FAO Penman-Monteith. The UI's weather-fill action uses Open-Meteo daily ET0 and **daily forecast rain**, not current-interval rain. Temperature/humidity are provider current estimates; this mixed current/forecast daily scenario is disclosed in the UI.
- Legacy assumptions (uncalibrated): effective rain = 0.8 × daily rain; initial soil credit = max(0, moisture − 15) × 0.5 mm; application efficiency = 0.75. The moisture conversion is a demonstration proxy, not a measured volumetric root-zone balance. No soil-depth, rooting-depth or field-capacity calibration is available.
- Daily net deficit = max(0, ETc − effective rain − initial soil credit). Gross depth = net depth / efficiency. **1 mm × 1 ha = 10,000 L = 10 m³**; efficiency is applied exactly once. UI/report distinguish estimated water balance from the final action's zero/nonzero depth/volume.
- Final irrigation requires a positive raw ML recommendation **and** positive daily water deficit, with no safety override. Moisture **>80%** or daily rain **>30 mm** blocks irrigation. These inherited demo thresholds are not new locally validated thresholds. Waterlogging is separated from deficit stress. Raw model recommendation and final rule-based decision are displayed separately; final blocked actions have zero recommended water.
- Seven-day scenario uses actual dated provider forecast ET0/rain and the same crop/stage/efficiency convention. Initial soil credit is applied **once**, remaining credit/rain surplus is carried forward, deficits are treated as hypothetically replenished each day. No repeated moisture reset, double efficiency, runoff/root-zone capacity/drainage simulation or future ML decision is claimed. It is a **potential water-balance scenario, not scheduled irrigation**; daily field verification and safety overrides still apply. No forecast means no seven-day numbers. It is intentionally not extrapolated from a single manually entered day.
- Risk scores are inherited heuristic 0–100 indices, not probabilities or observed damage. Overall <=35 low; >35 through 70 medium; >70 high. Yield-risk uses tree spread and weather indices, not a validated outcome model. Heatwave utility checks three **consecutive dated** maxima >35°C, not merely three scattered hot days; this is also a legacy demonstration threshold.

## UI and settings

Non-sensitive preferences (default location, refresh interval 5/15/30/60 minutes, language) are validated, saved locally, restored after reload and resettable. Saving the default changes the main location selector. Refresh requests run while the page is visible; the server cache remains fixed at 30 minutes. No API-key, unimplemented imperial units, notification preference or configurable cache controls are advertised. Alerts are derived only from the current analysis. Soil moisture is **never automatically claimed as measured**: enter a value, report a sensor reading yourself, or explicitly select the uncalibrated heuristic. No sensor integration exists.

Failed weather/analysis requests show errors and clear affected results. Inputs changed during an in-flight analysis invalidate its display; a successfully completed request may still appear in history. Browsers use non-secret localStorage preferences, not accounts. All charts/tables read backend values, no standalone frontend irrigation formula. Fonts, icons and charts do not require a CDN; Lucide 0.468.0 is vendored with its ISC/MIT notices. English/Russian/Tajik navigation remains; scientific disclosures and some new technical feedback intentionally remain English.

## API and reports

| Route | Purpose |
|---|---|
| `GET /` | Dashboard |
| `GET /api/health` | HTTP 200 healthy models/storage, 503 degraded; no internal paths |
| `GET /api/data-sources` | Stable provenance JSON; unavailable/warning states without invented counts |
| `GET /api/locations` | Configured Tajikistan locations |
| `GET /api/weather?location=dushanbe` | Validated provider weather/cache, 503 if unavailable, 422 unknown location |
| `POST /api/decision` | Validate, infer, fuse, persist; all significant decisions in response |
| `POST /api/predict` | Compatibility alias for decision |
| `GET /api/history?limit=100` | Latest persisted predictions, bounded 1–1000, legacy provenance labelled |
| `GET /api/report?format=csv&report_type=full&period=all&limit=100` | Filtered CSV |

Report types: `full`, `water` (estimated requirements, not metered consumption), `irrigation`, `risk`, `yield`. Periods: trailing `7`, `30`, `90` days or `all`; UTC inclusive boundaries, filtering before the 1–1000 row limit. New timestamps are timezone-aware UTC. Legacy naive timestamps are **assumed UTC because their original timezone is unknown**, and original database values are not rewritten. Historical legacy predictions/model provenance cannot be retrospectively verified. CSV is UTF-8 with BOM, escaped quoting and spreadsheet-formula protection. Empty reports contain headers only. Invalid filters return 422. CSV exports are not PDFs, compliance certifications or a persisted report-generation history. No measured water savings are claimed. The dashboard history counter is the latest 100 records, not an invented all-time total.

API exploration: http://127.0.0.1:8000/docs on your own running installation. For a manual, no-weather-dependency analysis, `POST /api/decision`:

```json
{"location":"Manual demonstration scenario","temperature":40,"rainfall":0,"humidity":20,"soil_moisture":10,"soil_moisture_source":"manual","field_size":2,"crop_type":"Cotton","soil_type":"Loamy","growth_stage":"Mid-Season"}
```

This is a **declared hypothetical input scenario**, not invented live weather. It produces a saved analysis, but no seven-day forecast plan. Supply `weather_location:"dushanbe"` to request a real provider forecast scenario; forecast failure does not fabricate a plan or prevent manual analysis.

## Tests

Windows PowerShell, from `swip`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check main.py services models/train.py database/db.py tests
.\.venv\Scripts\python.exe -m compileall -q main.py services models database tests
node --check static/js/app.js
node --check static/js/charts.js
node --check static/js/preferences.js
node --test tests/preferences.test.cjs
```

On Linux, substitute `.venv/bin/python`. Unit/integration tests isolate SQLite and mock weather only **inside tests**; operational weather is never mocked. Browser interaction, live HTTP and container verification results are separate from pytest; see the implementation report for actual executed checks. Windows commands are documented but Windows execution must not be inferred from Linux success.

## Docker (local demonstration)

From `swip`, with Docker Engine/Desktop and Compose available:

```sh
docker compose build --no-cache
docker compose up -d
docker compose ps
docker compose logs swip
docker compose down
```

Open http://127.0.0.1:8000 on the Docker host. The image uses Python 3.11.15, locked dependencies, packaged operational pipelines, a non-root runtime user and an HTTP model/storage healthcheck. Compose binds **only to loopback**, with a named `swip_history` volume at `/data`. `down` preserves history; **do not use `down -v`** unless you explicitly intend to delete that volume. Containers start a new empty volume; local source SQLite files and secrets are excluded from the image. To import local history, stop the app and back up/copy your chosen DB into the volume with suitable ownership (UID/GID 10001). Never overwrite an existing volume's DB without a backup and deliberate migration plan. No unnecessary Nginx/reverse proxy is included. No public deployment, TLS/authentication, multi-user isolation, OS vulnerability scan or production readiness is claimed.

## Competition flow (honest, reproducible)

1. Start locally; check health/provenance. Explain synthetic generated targets and lack of real field validation before showing scores.
2. Select a Tajikistan location. If Open-Meteo responds, show source, retrieval time, cache age and the actual forecast. If it is unavailable, show that state; never present hypothetical numbers as live.
3. In Predictor, explicitly fill available weather or enter the declared manual scenario above. Enter crop/stage/area and your moisture source. Submit once; show **raw model versus final decision**, net/gross units, yield limitation and reasons.
4. Repeat with moisture 90% to demonstrate the waterlogging safety block; final irrigation and final recommended water must be zero even if the raw model suggests irrigation.
5. With an available real forecast, open Water Management: inspect seven actual dated rows and the backend net/gross totals. Without external weather, demonstrate the truthful unavailable plan; do not claim this portion succeeded.
6. Open History, distinguish legacy/unverified records from new synthetic-model estimates, then export a chosen report type, UTC period, format and limit. Inspect the real CSV. Save/reload/reset browser preferences and demonstrate mobile Menu.

## Remaining validation needs and troubleshooting

- A controlled agricultural pilot requires consented field-level observations: measured soil-water profiles and calibration, local weather, actual irrigation timing/volumes, drainage/soil properties, crop stage/management and independently observed yields. Evaluate across fields/seasons with independent splits and appropriate agronomic oversight before claiming benefit or safe guidance. Do not use this demonstration to operate irrigation autonomously.
- Weather 503: verify Internet/provider status; use manual daily inputs or wait for real weather. Stale data is not an observation or a forecast refresh. No fabricated fallback exists.
- Models 503: install `requirements.lock` in Python 3.11, verify both operational files and matching metadata came from the same trusted commit, and restart. Do not suppress compatibility warnings or substitute legacy artifacts. Deliberate retraining is documented above.
- Storage 503: check `SWIP_DB_PATH`, disk space and permissions. Stop/backup before changing DB files. Additive startup migration preserves old rows.
- Settings cannot save: browser storage may be blocked/corrupt. A visible warning and defaults are used; correct settings and save again. Only preferences, not project data or secrets, are stored in localStorage.
- This app has no user authentication. Keep it loopback/local; do not expose farm data to a public network. A successful dependency advisory check is point-in-time evidence, not a security guarantee.
