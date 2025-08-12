# control/auto_navigation.py
"""
Auto navigation wrappers.
Use the provided `send` callable to instruct the bridge to set control mode.
The ESP switches behaviour based on messages on /control_mode.
"""

def start_auto(send):
    """Switch robot to autonomous mode."""
    if callable(send):
        send({"type": "mode", "data": "auto"})

def stop_auto(send):
    """Switch robot back to manual mode (and stop auto behaviour)."""
    if callable(send):
        send({"type": "mode", "data": "manual"})
