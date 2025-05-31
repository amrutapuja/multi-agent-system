# router/action_router.py
import requests
from datetime import datetime

def route_action(agent_result: dict, classification: dict):
    action = agent_result.get("action")
    simulated_endpoint = ""
    response = {}

    if action == "escalate":
        simulated_endpoint = "/crm/escalate"
        response = {"status": "escalated", "ticket_id": "CRM123"}
    elif action == "flag_risk":
        simulated_endpoint = "/risk_alert"
        response = {"status": "risk_flagged", "alert_id": "RISK456"}
    elif action == "log_alert":
        simulated_endpoint = "/log/alert"
        response = {"status": "anomaly_logged"}
    else:
        simulated_endpoint = "/log/general"
        response = {"status": "logged"}

    return {
        "action": action,
        "simulated_endpoint": simulated_endpoint,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    }