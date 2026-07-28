def calculate_risk_score(soil_moisture, temperature, rainfall):
    score = 0
    
    # Soil Moisture Risk (0-40 points)
    if soil_moisture < 20:
        score += 40
    elif soil_moisture < 40:
        score += 20
    else:
        score += 0
        
    # Temperature Risk (0-30 points)
    if temperature > 35:
        score += 30
    elif temperature > 25:
        score += 15
    else:
        score += 0
        
    # Rainfall Risk (0-30 points)
    if rainfall < 5:
        score += 30
    elif rainfall < 20:
        score += 15
    else:
        score += 0
        
    # Ensure it is bounded 0-100
    score = min(max(score, 0), 100)
    
    level = "LOW"
    if score > 70:
        level = "HIGH"
    elif score > 30:
        level = "MEDIUM"
        
    return {
        "risk_score": score,
        "risk_level": level
    }
