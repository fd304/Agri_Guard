import logging
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel, ConfigDict, Field, model_validator

from database.db import database_available, get_recent_predictions, init_db, insert_prediction
from services.alert_engine import alert_engine
from services.data_sources import get_data_sources
from services.decision_engine import decision_engine
from services.ml_engine import ModelUnavailableError, ml_engine
from services.report_service import report_service
from services.weather_service import LOCATIONS, WeatherUnavailableError, weather_service

ROOT = Path(__file__).resolve().parent
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    try:
        init_db()
    except (sqlite3.Error, OSError):
        logger.error('History storage unavailable. Verify SWIP_DB_PATH permissions.')
    yield


app = FastAPI(title='Smart Water Intelligence Platform (SWIP)', lifespan=lifespan)
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')
templates = Jinja2Templates(directory=ROOT / 'templates')


@app.middleware('http')
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'same-origin'
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    return JSONResponse(status_code=422, content={'detail': [
        {'loc': list(error['loc']), 'msg': error['msg'], 'type': error['type']} for error in exc.errors()]})


class DecisionRequest(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False, extra='forbid', str_strip_whitespace=True, strict=True)
    location: str = Field('Unspecified manual location', min_length=1, max_length=120)
    weather_location: str | None = Field(None, max_length=30)
    temperature: float = Field(ge=-30, le=60)
    rainfall: float = Field(ge=0, le=500, description='Daily precipitation in mm, not current-interval rain')
    humidity: float = Field(ge=0, le=100)
    soil_moisture: float | None = Field(None, ge=0, le=100)
    soil_moisture_source: Literal['manual', 'estimated', 'sensor'] = 'manual'
    field_size: float = Field(gt=0, le=10000)
    crop_type: Literal['Cotton', 'Wheat', 'Tomato', 'Potato', 'Onion', 'Cucumber']
    soil_type: Literal['Sandy', 'Loamy', 'Clay']
    growth_stage: Literal['Initial', 'Development', 'Mid-Season', 'Late-Season'] = 'Mid-Season'
    et0_mm: float | None = Field(None, ge=0, le=30)
    language: Literal['en', 'ru', 'tg'] = 'en'

    @model_validator(mode='after')
    def validate_sources(self):
        if self.soil_moisture_source != 'estimated' and self.soil_moisture is None:
            raise ValueError('Enter a soil-moisture value or explicitly choose the heuristic estimate.')
        if self.weather_location is not None and self.weather_location not in LOCATIONS:
            raise ValueError('Unknown forecast location')
        return self


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@app.get('/api/health')
def health():
    database_ok = database_available()
    healthy = ml_engine.available and database_ok
    return JSONResponse(status_code=200 if healthy else 503, content={
        'status': 'ok' if healthy else 'degraded',
        'models': 'available' if ml_engine.available else 'unavailable',
        'database': 'available' if database_ok else 'unavailable',
        'model_version': ml_engine.model_version if ml_engine.available else None,
        'weather': 'External dependency; availability checked per request',
        'readiness': 'Demonstration only; no field validation',
    })


@app.get('/api/data-sources')
def data_sources():
    return get_data_sources(model_available=ml_engine.available)


@app.get('/api/locations')
async def get_locations():
    return await weather_service.get_locations()


@app.get('/api/weather')
async def get_weather(location: str = Query(min_length=1, max_length=30)):
    if location not in LOCATIONS:
        raise HTTPException(422, 'Unknown location. Choose a location from /api/locations.')
    try:
        return await weather_service.get_weather_for_location(location)
    except WeatherUnavailableError as exc:
        raise HTTPException(503, str(exc)) from None


@app.post('/api/decision')
async def get_decision(req: DecisionRequest):
    if not ml_engine.available:
        raise HTTPException(503, 'Models unavailable. Verify packaged pipelines and pinned dependencies; no prediction was generated.')
    weather = None
    if req.weather_location:
        try:
            candidate = await weather_service.get_weather_for_location(req.weather_location)
            if not candidate['stale']:
                weather = candidate
        except WeatherUnavailableError:
            pass  # Manual analysis remains possible; the plan is explicitly unavailable.
    try:
        decision = await run_in_threadpool(decision_engine.evaluate, req, weather)
    except ModelUnavailableError:
        raise HTTPException(503, 'Model inference failed validation; no prediction was stored.') from None
    except Exception:
        logger.error('Decision evaluation failed; no prediction stored.')
        raise HTTPException(500, 'Analysis failed. Check inputs and the documented runtime environment.') from None
    decision['alerts'] = alert_engine.generate_alerts(decision, weather)
    record = req.model_dump(exclude={'language', 'weather_location', 'et0_mm'})
    record.update(soil_moisture=decision['soil_status']['moisture_percent'],
                  soil_moisture_source=decision['soil_status']['source'],
                  prediction=int(decision['irrigation']['recommended']),
                  raw_recommended=int(decision['model_irrigation']['recommended']),
                  yield_prediction=decision['yield']['prediction_t_ha'], risk_score=decision['risk']['overall'],
                  water_required=decision['irrigation']['water_liters'],
                  net_irrigation_mm=decision['water_balance']['amount_mm'],
                  model_version=decision['model_version'], decision_json=decision)
    try:
        decision['history_id'] = await run_in_threadpool(insert_prediction, record)
    except (sqlite3.Error, OSError):
        raise HTTPException(503, 'History storage unavailable; analysis was not saved. Retry after storage is restored.') from None
    return decision


@app.get('/api/history')
def history(limit: int = Query(100, ge=1, le=1000)):
    try:
        return {'history': get_recent_predictions(limit), 'timezone': 'UTC',
                'warning': 'Legacy records have unverified provenance. Legacy naive timestamps are treated as UTC; original timezone is unknown.'}
    except sqlite3.Error:
        raise HTTPException(503, 'History storage unavailable.') from None


@app.get('/api/report')
def get_report(format: Literal['csv'] = 'csv', limit: int = Query(100, ge=1, le=1000),
               report_type: Literal['full', 'water', 'irrigation', 'risk', 'yield'] = 'full',
               period: Literal['7', '30', '90', 'all'] = 'all'):
    try:
        records = get_recent_predictions(limit, period=period)
        csv_data = report_service.generate_csv_report(records, report_type)
    except sqlite3.Error:
        raise HTTPException(503, 'Report unavailable because history storage could not be read.') from None
    return Response(content=csv_data, media_type='text/csv; charset=utf-8', headers={
        'Content-Disposition': f'attachment; filename="swip_{report_type}_{period}.csv"',
        'X-Report-Record-Count': str(len(records)), 'X-Report-Timezone': 'UTC'})


@app.post('/api/predict')
async def predict_compat(req: DecisionRequest):
    return await get_decision(req)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
