def generate_explanation(is_recommended, probability, risk, water_req, lang="en"):
    """
    Generate human-readable explanations based on the decision engine outputs.
    """
    reasons = []
    
    texts = {
        "en": {
            "high_conf_irrigate": f"ML Model confidence for irrigation is high ({probability}%).",
            "deficit": f"Agronomic models estimate a deficit of {water_req['amount_mm']} mm.",
            "drought_risk": "High drought risk factor contributes to this recommendation.",
            "heat_stress": "High heat stress is elevating crop water demand.",
            "water_stress": "Low soil moisture is causing crop water stress.",
            "high_conf_wait": f"ML Model confidence against irrigation is high ({(100 - probability):.1f}%).",
            "suff_moisture": "Current soil moisture and rainfall are sufficient.",
            "flood_risk": "High heavy rain/flood risk; additional irrigation is strongly discouraged."
        },
        "ru": {
            "high_conf_irrigate": f"Уверенность ML-модели в необходимости полива высока ({probability}%).",
            "deficit": f"Агрономические модели оценивают дефицит в {water_req['amount_mm']} мм.",
            "drought_risk": "Высокий фактор риска засухи способствует этой рекомендации.",
            "heat_stress": "Высокий тепловой стресс повышает потребность культур в воде.",
            "water_stress": "Низкая влажность почвы вызывает водный стресс у культур.",
            "high_conf_wait": f"Уверенность ML-модели в отсутствии необходимости полива высока ({(100 - probability):.1f}%).",
            "suff_moisture": "Текущей влажности почвы и осадков достаточно.",
            "flood_risk": "Высокий риск проливных дождей/наводнения; дополнительный полив настоятельно не рекомендуется."
        },
        "tg": {
            "high_conf_irrigate": f"Боварии модели ML барои обёрӣ баланд аст ({probability}%).",
            "deficit": f"Моделҳои агрономӣ норасоиро дар сатҳи {water_req['amount_mm']} мм арзёбӣ мекунанд.",
            "drought_risk": "Омили хавфи баланди хушксолӣ ба ин тавсия мусоидат мекунад.",
            "heat_stress": "Стресси гармии баланд талаботи зироатро ба об зиёд мекунад.",
            "water_stress": "Намнокии пасти хок боиси стресси обии зироат мегардад.",
            "high_conf_wait": f"Боварии модели ML ба муқобили обёрӣ баланд аст ({(100 - probability):.1f}%).",
            "suff_moisture": "Намнокии кунунии хок ва боришот кифоя аст.",
            "flood_risk": "Хавфи баланди боришоти шадид/обхезӣ; обёрии иловагӣ қатъиян тавсия дода намешавад."
        }
    }
    
    t = texts.get(lang, texts["en"])
    
    if is_recommended:
        reasons.append(t["high_conf_irrigate"])
        if water_req["amount_mm"] > 0:
            reasons.append(t["deficit"])
        if risk["drought"] > 50:
            reasons.append(t["drought_risk"])
        if risk["heat"] > 50:
            reasons.append(t["heat_stress"])
        if risk["water_stress"] > 50:
            reasons.append(t["water_stress"])
    else:
        reasons.append(t["high_conf_wait"])
        if water_req["amount_mm"] == 0:
            reasons.append(t["suff_moisture"])
        if risk["flood"] > 50:
            reasons.append(t["flood_risk"])
            
    return reasons

