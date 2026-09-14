from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn
import os
import json

from services.decision_engine import decision_engine
from services.weather_service import weather_service
from services.alert_engine import alert_engine
from services.report_service import report_service
from database.db import init_db, insert_prediction, get_recent_predictions

app = FastAPI(title="Smart Water Intelligence Platform (SWIP)")

# Ensure database is initialized
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ==========================================
# SCHEMAS
# ==========================================
class DecisionRequest(BaseModel):
    location: str = Field("Unknown", description="Name of the location")
    temperature: float = Field(..., ge=-30, le=60, description="Temperature in Celsius")
    rainfall: float = Field(..., ge=0, le=500, description="Rainfall in mm")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    soil_moisture_source: str = Field("manual", description="Source: manual, estimated, sensor")
    field_size: float = Field(..., gt=0, le=10000, description="Field size in Hectares")
    crop_type: str = Field(..., description="Type of crop")
    soil_type: str = Field(..., description="Type of soil")
    growth_stage: str = Field("Mid-Season", description="Growth stage of crop")
    language: str = Field("en", description="Interface language")

# ==========================================
# ENDPOINTS
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.get("/api/locations")
async def get_locations():
    return await weather_service.get_locations()

@app.get("/api/weather")
async def get_weather(location: str):
    return await weather_service.get_weather_for_location(location)

@app.post("/api/decision")
async def get_decision(req: DecisionRequest):
    # Retrieve current weather context internally if needed, 
    # but the req object contains the live/user-submitted inputs for the engine.
    
    # 1. Get Core Decision Payload
    try:
        decision = decision_engine.evaluate(req, None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    # 2. Get Alerts
    alerts = alert_engine.generate_alerts(decision, None)
    decision["alerts"] = alerts
    
    # 3. Save to History
    db_record = {
        "location": req.location,
        "temperature": req.temperature,
        "rainfall": req.rainfall,
        "humidity": req.humidity,
        "soil_moisture": decision["soil_status"]["moisture_percent"],
        "soil_type": req.soil_type,
        "crop_type": req.crop_type,
        "field_size": req.field_size,
        "prediction": 1 if decision["irrigation"]["recommended"] else 0,
        "yield_prediction": decision["yield"]["prediction_t_ha"],
        "risk_score": decision["risk"]["overall"],
        "water_required": decision["irrigation"]["water_liters"]
    }
    insert_prediction(db_record)
    
    return decision

@app.get("/api/history")
async def history(limit: int = 100):
    records = get_recent_predictions(limit)
    return {"history": records}

@app.get("/api/report")
async def get_report(format: str = "csv", limit: int = 100):
    records = get_recent_predictions(limit)
    if format.lower() == "csv":
        csv_data = report_service.generate_csv_report(records, "full")
        return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=swip_report.csv"})
    else:
        raise HTTPException(status_code=400, detail="Only CSV format is currently supported.")

# Keep /api/predict for backwards compatibility, redirect to decision
@app.post("/api/predict")
async def predict_compat(req: DecisionRequest):
    return await get_decision(req)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
