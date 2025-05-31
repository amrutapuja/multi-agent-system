import json
from pydantic import BaseModel, ValidationError
from datetime import datetime

# Define expected schema
class WebhookEvent(BaseModel):
    event: str
    amount: float
    location: str

def process_json(file_content: bytes):
    try:
        content = json.loads(file_content.decode("utf-8"))
        validated = WebhookEvent(**content)
        anomaly = False
        issues = []
    except ValidationError as ve:
        anomaly = True
        issues = ve.errors()
        validated = None
    except Exception as e:
        anomaly = True
        issues = [str(e)]
        validated = None

    return {
        "source": "json",
        "anomaly_detected": anomaly,
        "issues": issues if anomaly else None,
        "parsed_data": content if not anomaly else None,
        "action": "log_alert" if anomaly else "log"
    }
