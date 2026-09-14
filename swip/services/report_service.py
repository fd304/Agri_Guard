import io
import csv
from datetime import datetime

class ReportService:
    def __init__(self):
        pass

    def generate_csv_report(self, history_records, report_type):
        """
        Generates a CSV string containing the requested history records.
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "Timestamp", "Location", "Crop Type", "Soil Type", 
            "Temperature (C)", "Rainfall (mm)", "Soil Moisture (%)",
            "Irrigation Recommended", "Water Required (Liters)", "Risk Score"
        ])
        
        for record in history_records:
            # Based on the db record structure we'll define later
            writer.writerow([
                record.get("timestamp", ""),
                record.get("location", "Unknown"),
                record.get("crop_type", ""),
                record.get("soil_type", ""),
                record.get("temperature", ""),
                record.get("rainfall", ""),
                record.get("soil_moisture", ""),
                "Yes" if record.get("prediction") == 1 else "No",
                record.get("water_required", ""),
                record.get("risk_score", "")
            ])
            
        return output.getvalue()

report_service = ReportService()
