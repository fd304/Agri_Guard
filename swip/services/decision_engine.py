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
        
        et0 = request_data.et0_mm if request_data.et0_mm is not None else feature_engineering.calculate_et0(temp, humidity)
        
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
        override = 'waterlogging' if soil_moisture > 80 else 'heavy_rain' if rain > 30 else None
        is_recommended = bool(not override and irrigation_prediction["recommended"] and water_req["amount_mm"] > 0)
        reasons = ([override] if override else
                   ['model_and_water_deficit'] if is_recommended else
                   ['no_water_deficit'] if water_req['amount_mm'] == 0 else ['model_does_not_recommend'])

        # 8. Explainability
        explanations = generate_explanation(
            is_recommended, irrigation_prediction["probability"], risk, water_req, request_data.language,
            raw_recommended=irrigation_prediction['recommended'], override=override
        )

        return {
            'decision': {'state': 'IRRIGATE' if is_recommended else 'DO_NOT_IRRIGATE',
                         'reasons': reasons, 'safety_override': override,
                         'policy': 'Demonstration rules; confirm conditions before field use'},
            'model_irrigation': irrigation_prediction,
            'model_version': ml_engine.model_version,
            'water_balance': water_req,
            'plan': water_calculator.seven_day_plan(current_weather['forecast'], soil_moisture,
                        request_data.field_size, request_data.crop_type, growth_stage)
                    if current_weather else {'status': 'unavailable', 'days': [],
                        'meaning': 'No validated live forecast available; no seven-day values generated.'},
            "irrigation": {
                "recommended": is_recommended,
                "probability_percent": irrigation_prediction["probability"],
                "amount_mm": water_req["amount_mm"] if is_recommended else 0,
                "water_liters": water_req["water_liters"] if is_recommended else 0,
                "priority": water_req["priority"] if is_recommended else 'LOW'
            },
            "yield": yield_prediction,
            "risk": risk,
            "weather_features": {
                "et0_mm": et0,
                "et0_source": 'User-supplied daily reference ET0' if request_data.et0_mm is not None else 'Uncalibrated temperature/humidity heuristic',
                "water_deficit_mm": water_req['amount_mm']
            },
            "soil_status": {
                "moisture_percent": soil_moisture,
                "source": soil_data["source"]
            },
            "explanations": explanations
        }

decision_engine = DecisionEngine()
