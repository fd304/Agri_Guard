from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os

from services.ml_engine import ml_engine
from services.risk_engine import calculate_risk_score
from services.explainability import generate_explanation
from services.water_calculator import calculate_water_requirement
from database.db import init_db, insert_prediction, get_recent_predictions

app = FastAPI(title="Smart Water Intelligence Platform (SWIP)")

# Ensure database is initialized
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class PredictionRequest(BaseModel):
    temperature: float
    rainfall: float
    humidity: float
    soil_moisture: float
    field_size: float
    crop_type: str
    soil_type: str
    language: str = "tg"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/api/predict")
async def predict(req: PredictionRequest):
    # ML Prediction
    prediction = ml_engine.predict(
        req.temperature, req.rainfall, req.humidity, 
        req.soil_moisture, req.field_size, req.crop_type, req.soil_type
    )
    
    # Risk Score
    risk = calculate_risk_score(req.soil_moisture, req.temperature, req.rainfall)
    
    # Explanation
    explanation = generate_explanation(prediction, req.soil_moisture, req.temperature, req.rainfall, req.language)
    
    # Water Requirement
    water_req = calculate_water_requirement(req.field_size, req.crop_type, req.soil_moisture)
    
    response_data = {
        "prediction": prediction,
        "recommendation": "Irrigate" if prediction == 1 else "Do Not Irrigate",
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "water_required_liters": water_req["water_required_liters"],
        "reasons": explanation
    }
    
    # Save to database
    db_data = req.dict()
    db_data.update({
        "prediction": prediction,
        "risk_score": risk["risk_score"],
        "water_required": water_req["water_required_liters"]
    })
    insert_prediction(db_data)
    
    return response_data

@app.get("/api/history")
async def history(limit: int = 100):
    records = get_recent_predictions(limit)
    return {"history": records}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
