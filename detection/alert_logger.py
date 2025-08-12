# detection/alert_logger.py

import time

# Severity mapping for known hazard classes
SEVERITY_MAP = {
    "asap": "High",         # smoke/fire
    "api": "High",          # smoke/fire
    "gas": "High",
    "leak": "Moderate",
    "crack": "Moderate",
    "damage": "Moderate",
    "hardhat": "Low",
    "safety_boots": "Low",
    "safety_gloves": "Low",
    "safety_mask": "Low",
    "safety_vest": "Low",
    "person": "Low",        # may be upgraded if PPE missing
}

alerts = []

def log_detection(label, location="Unknown", ppe_violation=False):
    """
    Log a detection with timestamp, label, severity, and location.
    :param label: Detected object label
    :param location: Location string (default 'Unknown')
    :param ppe_violation: If True, auto-upgrade severity for missing PPE
    """
    timestamp = time.strftime("%H:%M:%S")
    label_lower = str(label).lower()

    # Determine severity from map
    severity = SEVERITY_MAP.get(label_lower, "Moderate")

    # Upgrade to Moderate if PPE violation detected for a person
    if label_lower == "person" and ppe_violation:
        severity = "Moderate"

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
