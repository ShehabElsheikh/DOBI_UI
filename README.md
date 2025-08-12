# DOBI_UI

DOBI_UI is a modular and interactive **robot control and monitoring interface** built with **Streamlit**, designed to run on Raspberry Pi Ubuntu 22.  
It connects with a ROS 2 + micro-ROS pipeline to control a robot via **manual joystick-style controls** or **automatic navigation**, while providing **real-time feedback** from onboard sensors and YOLO-based object detection.

---

## 🚀 Features

- **Manual Mode:**  
  Direct control of the robot's motors via on-screen buttons or joystick interface (commands sent to ESP32 via ROS 2 bridge).
  
- **Automatic Mode:**  
  Pre-programmed autonomous navigation logic — path following, obstacle avoidance, and other behaviors handled by the robot firmware.

- **YOLO Object Detection:**  
  Uses Ultralytics YOLO models for real-time object recognition from a connected camera stream.

- **ROS 2 WebSocket Bridge:**  
  A FastAPI WebSocket server acts as a bridge between the UI and ROS 2 topics, allowing full two-way communication.

- **Configurable Parameters:**  
  Adjustable settings for movement speed, detection confidence thresholds, and camera source.

- **Modular Code Structure:**  
  Control logic, UI elements, ROS interface, and detection modules are separated for easy maintenance.

---

## 📂 Project Structure

```
DOBI_UI/
│
├── bridge/ # WebSocket bridge for UI ↔ ROS2
│ ├── server.py # FastAPI WebSocket server
│ ├── ros_node.py # ROS 2 node handling subscriptions & publishing
│
├── control/ # Robot control logic
│ ├── manual_control.py # Manual driving functions
│ ├── auto_navigation.py # Autonomous control functions
│
├── detection/ # Object detection
│ ├── yolov8_detector.py # Ultralytics YOLO model integration
│
├── ui/ # Streamlit UI components
│ ├── camera_stream.py # Camera feed handling
│ ├── control_panel.py # UI widgets for robot control
│
├── config.py # User-configurable settings
├── main.py # Streamlit app entry point
├── requirements.txt # Python dependencies
├── run_bridge.sh # Launch script for WebSocket bridge
└── README.md
```
---
## ⚙️ Installation

> **Note:** This guide assumes ROS 2 and micro-ROS are already installed and configured on your Raspberry Pi.

1. **Clone the repository**
```
git clone 
cd 
```
2. **Install system dependencies**
```
sudo apt update
sudo apt install python3-pip python3-venv

```

3. **Create and activate a Python virtual environment**
```
python3 -m venv venv
source venv/bin/activate
```

4. **Install Python dependencies**
```
pip install --upgrade pip
pip install -r requirements.txt
```
---


## 🛠 Configuration

The `config.py` file contains all adjustable parameters:

### Camera Settings
```python
CAMERA_SOURCE = 0  # 0 for default webcam, or a video stream URL
```

## YOLO Settings
```python
YOLO_MODEL_PATH = "yolov8n.pt"  # Path to YOLO model
DETECTION_CONFIDENCE = 0.5      # Minimum detection confidence
```

## Robot Movement
```python
SPEED_LINEAR = 0.5
SPEED_ANGULAR = 0.3
```

## ▶️ Running the UI
Start the ROS 2 WebSocket Bridge
```python
bash run_bridge.sh
```
Launch the Streamlit UI
```python
streamlit run main.py --server.port 8501
```

Open your browser and go to:
```python
http://<raspberrypi-ip>:8501
```
---
## 🔌 Manual vs Automatic Mode
**Manual Mode:**

Allows direct driving via UI controls.

Commands are sent directly to the ESP firmware via ROS 2 topics.

**Automatic Mode:**

Triggers the autonomous behavior on the ESP (navigation, avoidance).

The UI still receives sensor data and detection outputs in real time.

Mode switching is available from the control panel inside the UI.

---

## 📷 Object Detection

The UI integrates Ultralytics YOLOv8 for visual recognition.

Detected objects are displayed on the camera stream in real time.

Detection performance depends on your Raspberry Pi’s processing capability and the chosen YOLO model size.
