class AlertEngine:
    def __init__(self):
        pass

    def generate_alerts(self, decision_payload, forecast):
        alerts = []
        
        if decision_payload['risk'].get('waterlogging', 0):
            alerts.append({'type': 'danger', 'title': 'Possible waterlogging',
                           'desc': 'Irrigation blocked by the demonstration moisture rule; verify field drainage.'})
        
        # 2. Risk Alerts
        risk = decision_payload["risk"]
        
        if risk["heat"] > 70:
            alerts.append({
                "type": "danger",
                "title": "High Heat Stress Alert",
                "desc": "Current or forecast temperatures are elevating crop water requirements significantly."
            })
            
        if risk["drought"] > 70:
            alerts.append({
                "type": "warning",
                "title": "Drought Risk Alert",
                "desc": "The submitted daily temperature and rainfall trigger the heuristic dryness index; prolonged drought is not established."
            })
            
        if risk["flood"] > 70:
            alerts.append({
                "type": "danger",
                "title": "Heavy Rain Alert",
                "desc": "Significant precipitation expected. Pause irrigation and monitor for waterlogging."
            })
            
        # 3. Irrigation Alert
        if decision_payload["irrigation"]["recommended"] and decision_payload["irrigation"]["amount_mm"] > 15:
            alerts.append({
                "type": "info",
                "title": "Action Required: Irrigation",
                "desc": f"Large water deficit detected ({decision_payload['irrigation']['amount_mm']} mm). Please schedule irrigation."
            })
            
        return alerts

alert_engine = AlertEngine()
