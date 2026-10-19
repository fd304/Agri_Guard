def generate_explanation(is_recommended, probability, risk, water_req, lang='en', *, raw_recommended=False, override=None):
    prefixes = {'en': 'Final rule-based decision', 'ru': 'Итоговое решение по правилам',
                'tg': 'Қарори ниҳоӣ аз рӯи қоидаҳо'}
    return [
        f"{prefixes.get(lang, prefixes['en'])}: {'IRRIGATE' if is_recommended else 'DO_NOT_IRRIGATE'}.",
        f"Raw synthetic-target model: {'irrigate' if raw_recommended else 'wait'}; uncalibrated class score {probability}% (not field success confidence).",
        f"Water-balance estimate: {water_req['amount_mm']} mm net, efficiency {water_req['efficiency']:.0%}. This is an uncalibrated daily approximation.",
        f"Safety override: {override or 'none'}. Thresholds (>80% moisture, >30 mm/day rain) are inherited demonstration assumptions, not locally validated guidance.",
        'All training inputs and targets are synthetic. No independent farm-outcome validation is available.',
    ]
