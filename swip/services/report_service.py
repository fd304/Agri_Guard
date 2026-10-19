import csv
import io

REPORT_FIELDS = {
    'full': [('timestamp', 'Timestamp (UTC)'), ('location', 'Location'), ('crop_type', 'Crop'),
             ('soil_type', 'Soil'), ('growth_stage', 'Growth stage'), ('field_size', 'Area (ha)'),
             ('temperature', 'Temperature (C)'), ('rainfall', 'Daily rainfall (mm)'), ('humidity', 'Humidity (%)'),
             ('soil_moisture', 'Soil moisture (%)'), ('soil_moisture_source', 'Moisture source'),
             ('raw_recommended', 'Raw model irrigate (1/0)'), ('prediction', 'Final irrigate (1/0)'),
             ('net_irrigation_mm', 'Estimated net deficit (mm)'), ('water_required', 'Final gross water (L)'),
             ('yield_prediction', 'Synthetic-model yield (t/ha)'), ('risk_score', 'Heuristic risk (0-100)'),
             ('model_version', 'Model version'), ('provenance', 'Record provenance')],
    'irrigation': [('timestamp', 'Timestamp (UTC)'), ('location', 'Location'), ('crop_type', 'Crop'),
                   ('field_size', 'Area (ha)'), ('raw_recommended', 'Raw model irrigate (1/0)'),
                   ('prediction', 'Final irrigate (1/0)'), ('net_irrigation_mm', 'Estimated net deficit (mm)'),
                   ('water_required', 'Final gross water (L)'), ('provenance', 'Record provenance')],
    'risk': [('timestamp', 'Timestamp (UTC)'), ('location', 'Location'), ('temperature', 'Temperature (C)'),
             ('rainfall', 'Daily rainfall (mm)'), ('soil_moisture', 'Soil moisture (%)'),
             ('risk_score', 'Heuristic risk (0-100)'), ('provenance', 'Record provenance')],
    'yield': [('timestamp', 'Timestamp (UTC)'), ('location', 'Location'), ('crop_type', 'Crop'),
              ('field_size', 'Area (ha)'), ('yield_prediction', 'Synthetic-model yield (t/ha)'),
              ('model_version', 'Model version'), ('provenance', 'Record provenance')],
}


def safe_cell(value):
    if value is None:
        return ''
    if isinstance(value, str) and (value.lstrip().startswith(('=', '+', '-', '@')) or value.startswith(('\t', '\r', '\n'))):
        return "'" + value
    return value


REPORT_FIELDS['water'] = REPORT_FIELDS['irrigation']


class ReportService:
    def generate_csv_report(self, history_records, report_type):
        if report_type not in REPORT_FIELDS:
            raise ValueError('Unknown report type')
        output = io.StringIO(newline='')
        writer = csv.writer(output)
        fields = REPORT_FIELDS[report_type]
        writer.writerow([label for _, label in fields])
        for record in history_records:
            writer.writerow([safe_cell(record.get(key)) for key, _ in fields])
        return '\ufeff' + output.getvalue()


report_service = ReportService()
