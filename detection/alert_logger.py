# detection/alert_logger.py

import time

alerts = []

def log_detection(label):
    timestamp = time.strftime("%H:%M:%S")
    # case-insensitive severity check
    severity = "High" if str(label).lower() in ("fire", "weapon") else "Moderate"
    location = "Unknown"
    alerts.append({
        "time": timestamp,
        "label": label,
        "severity": severity,
        "location": location
    })

def get_recent_alerts(n=10):
    return alerts[-n:][::-1]

def clear_alerts():
    alerts.clear()
