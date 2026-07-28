def generate_explanation(prediction, soil_moisture, temperature, rainfall, lang="en"):
    reasons = []
    
    # Translations dictionary
    texts = {
        "en": {
            "low_moisture": "Soil moisture is critically low.",
            "high_temp": "Temperature is above optimal range, increasing evaporation.",
            "low_rain": "Recent rainfall has been insufficient.",
            "irrigate_default": "Model predicts irrigation is necessary based on overall environmental factors.",
            "suff_moisture": "Soil moisture is currently sufficient.",
            "suff_rain": "Recent rainfall is adequate.",
            "no_irrigate_default": "Conditions are currently optimal; irrigation is not required at this time."
        },
        "ru": {
            "low_moisture": "Влажность почвы критически низкая.",
            "high_temp": "Температура выше оптимального диапазона, что увеличивает испарение.",
            "low_rain": "Недавних осадков было недостаточно.",
            "irrigate_default": "Модель прогнозирует необходимость полива на основе общих экологических факторов.",
            "suff_moisture": "В настоящее время влажность почвы достаточна.",
            "suff_rain": "Недавние осадки достаточны.",
            "no_irrigate_default": "В настоящее время условия оптимальны; полив не требуется."
        },
        "tg": {
            "low_moisture": "Намнокии хок хеле паст аст.",
            "high_temp": "Ҳарорат аз меъёр баланд аст ва бухоршавиро зиёд мекунад.",
            "low_rain": "Боришоти охирин нокифоя буд.",
            "irrigate_default": "Модел дар асоси омилҳои муҳити зист обёриро тавсия медиҳад.",
            "suff_moisture": "Дар айни замон намнокии хок кифоя аст.",
            "suff_rain": "Боришоти охирин кифоя аст.",
            "no_irrigate_default": "Дар айни замон шароит беҳтарин аст; обёрӣ лозим нест."
        }
    }
    
    # Fallback to English if language is not supported
    t = texts.get(lang, texts["tg"])
    
    if prediction == 1:
        if soil_moisture < 40:
            reasons.append(t["low_moisture"])
        if temperature > 30:
            reasons.append(t["high_temp"])
        if rainfall < 10:
            reasons.append(t["low_rain"])
        if not reasons:
            reasons.append(t["irrigate_default"])
    else:
        if soil_moisture >= 40:
            reasons.append(t["suff_moisture"])
        if rainfall >= 10:
            reasons.append(t["suff_rain"])
        if not reasons:
            reasons.append(t["no_irrigate_default"])
            
    return reasons
