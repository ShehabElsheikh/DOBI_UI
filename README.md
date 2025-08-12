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
      ┌─────────────┐       HTTP / WebSocket       ┌─────────────┐
      │  Streamlit  │ <--------------------------> │   Bridge    │
      │    UI App   │                              │ (FastAPI WS)│
      └─────────────┘                              └─────┬───────┘
                                                         │
                                          ROS 2 Python Node (rclpy)
                                                         │
                                     Publishes/subscribes ROS topics
                                                         ↓
                                              Other ROS 2 Nodes

```

## 📂 Directory Setup

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
git clone https://github.com/ShehabElsheikh/DOBI_UI
cd DOBI_UI
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
## 🖥 Installing the WebSocket Bridge (run_bridge.sh)

The `run_bridge.sh` script is included to automatically detect and launch the ROS 2 WebSocket bridge, no matter which ROS 2 distribution or Raspberry Pi setup you’re using.

**Installation Steps:**

1. **Make the script executable**
   ```bash
   chmod +x run_bridge.sh

2. **Start the ROS 2 WebSocket Bridge**
```python
bash run_bridge.sh
```

Automatically detects your ROS 2 installation (Foxy, Humble, Galactic, etc.).
Sources your ROS 2 environment.
Sources your workspace if found (~/ros2_ws/install/setup.bash).
Launches rosbridge_websocket on the default port 9090.

3. **Launch the Streamlit UI**
```python
streamlit run main.py --server.port 8501
```

4. **Open your browser and go to:**
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

---

## **⚠️ Alert Logging and Categorizing**

| Class Name                                                           | Severity                     | Reason                                                                                               |
| -------------------------------------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| **smoke / fire (asap/api)**                                          | **High**                     | Immediate danger to life and property, requires instant action.                                      |
| **gas**                                                              | **High**                     | Risk of explosion, suffocation, or poisoning.                                                        |
| **leak**                                                             | **Moderate**                 | Could indicate fluid, chemical, or fuel leak — hazard but not always instantly life-threatening.     |
| **crack**                                                            | **Moderate**                 | Structural integrity risk — urgent maintenance needed but not immediate danger unless critical size. |
| **damage**                                                           | **Moderate**                 | Could affect machinery, safety barriers, or structural parts — needs prompt repair.                  |
| **Person without PPE** *(detected indirectly via missing PPE items)* | **Moderate**                 | Unsafe work practice, risk of injury.                                                                |
| **Hardhat**                                                          | **Low** (positive detection) | Compliance item — low severity if present. High severity if absent in required zones.                |
| **Safety\_Boots**                                                    | **Low** (positive detection) | Same as above.                                                                                       |
| **Safety\_Gloves**                                                   | **Low**                      | Same as above.                                                                                       |
| **Safety\_Mask**                                                     | **Low**                      | Same as above unless in hazardous environment.                                                       |
| **Safety\_Vest**                                                     | **Low**                      | Same as above.                                                                                       |



