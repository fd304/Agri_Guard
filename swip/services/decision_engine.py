from .feature_engineering import feature_engineering
from .soil_service import soil_service
from .risk_engine import risk_engine
from .water_calculator import water_calculator
from .ml_engine import ml_engine
from .explainability import generate_explanation

class DecisionEngine:
    def __init__(self):
        pass

    def evaluate(self, request_data, current_weather):
        """
        Takes raw request data and current weather, and returns the authoritative
        JSON response with irrigation, yield, risk, and explanations.
        """
        # 1. Weather and Basic Features
        temp = request_data.temperature
        rain = request_data.rainfall
        humidity = request_data.humidity
        
        et0 = feature_engineering.calculate_et0(temp, humidity)
        
        # 2. Soil Moisture Processing
        soil_data = soil_service.process_soil_moisture(
            request_data.soil_moisture, 
            request_data.soil_moisture_source, 
            rain, 
            temp
        )
        soil_moisture = soil_data["value"]
        
        # 3. Growth Stage fallback if not provided
        growth_stage = request_data.growth_stage if hasattr(request_data, 'growth_stage') and request_data.growth_stage else "Mid-Season"

        # 4. ML Predictions
        yield_prediction = ml_engine.predict_yield(
            temp, rain, humidity, soil_moisture, request_data.field_size,
            request_data.crop_type, request_data.soil_type, growth_stage
        )
        
        irrigation_prediction = ml_engine.predict_irrigation(
            temp, rain, humidity, soil_moisture, request_data.field_size,
            request_data.crop_type, request_data.soil_type, growth_stage
        )

        # 5. Risk Assessment
        risk = risk_engine.calculate_risks(
            soil_moisture, temp, rain, request_data.crop_type, growth_stage, yield_prediction["range"]
        )

        # 6. Water Calculation
        water_req = water_calculator.calculate_irrigation_requirement(
            et0, rain, soil_moisture, request_data.field_size, request_data.crop_type, growth_stage
        )

        # 7. Merge Irrigation Recommendation
        # We combine ML recommendation with agronomic water requirement.
        # If ML says Irrigate AND agronomic need > 0, we irrigate.
        is_recommended = irrigation_prediction["recommended"] and water_req["amount_mm"] > 0

        # 8. Explainability
        explanations = generate_explanation(
            is_recommended, irrigation_prediction["probability"], risk, water_req, request_data.language
        )

        return {
            "irrigation": {
                "recommended": is_recommended,
                "probability_percent": irrigation_prediction["probability"],
                "amount_mm": water_req["amount_mm"],
                "water_liters": water_req["water_liters"],
                "priority": water_req["priority"]
            },
            "yield": yield_prediction,
            "risk": risk,
            "weather_features": {
                "et0_mm": et0,
                "water_deficit_mm": feature_engineering.calculate_water_deficit(et0, rain, soil_moisture)
            },
            "soil_status": {
                "moisture_percent": soil_moisture,
                "source": soil_data["source"]
            },
            "explanations": explanations
        }

decision_engine = DecisionEngine()
