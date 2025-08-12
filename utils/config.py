# utils/config.py
# Global configuration for DOBI_UI

# YOLO model
MODEL_PATH = "best.pt"
CAMERA_INDEX = 0
CONFIDENCE_THRESHOLD = 0.25

# Control mode: "ros" (default), "serial", or "both"
CONTROL_MODE = "ros"

# Serial fallback settings (only used if CONTROL_MODE includes "serial")
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

# Mapping from UI logical command -> payload sent to ESP (over ROS or serial)
# ESP expects single chars: 'w' (forward), 's' (back), 'a' (left), 'd' (right), 'x' (stop)
COMMAND_MAP = {
    "forward": "w",
    "backward": "s",
    "left": "a",
    "right": "d",
    "stop": "x"
}

# Bridge server settings
BRIDGE_HOST = "0.0.0.0"
BRIDGE_PORT = 8000

# Websocket ping interval (seconds)
WS_PING_INTERVAL = 0.5
