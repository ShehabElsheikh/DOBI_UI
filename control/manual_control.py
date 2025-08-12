# control/manual_control.py
"""
Manual control wrappers.
These functions accept a `send` callable which will be used to send the
logical command to the bridge (eg. ws_client.send).
This prevents direct hardware access from this module and keeps it testable.
"""

def move_forward(send):
    """Tell the bridge to move forward."""
    if callable(send):
        send({"type": "command", "data": "forward"})

def move_backward(send):
    """Tell the bridge to move backward."""
    if callable(send):
        send({"type": "command", "data": "backward"})

def turn_left(send):
    """Tell the bridge to turn left."""
    if callable(send):
        send({"type": "command", "data": "left"})

def turn_right(send):
    """Tell the bridge to turn right."""
    if callable(send):
        send({"type": "command", "data": "right"})

def stop(send):
    """Tell the bridge to stop."""
    if callable(send):
        send({"type": "command", "data": "stop"})
