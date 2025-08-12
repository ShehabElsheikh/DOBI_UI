# DOBI_UI

DOBI_UI is a Streamlit-based user interface for controlling and monitoring an autonomous inspection robot.  
It integrates with ROS 2 and micro-ROS to provide live video feed, control modes, and object detection capabilities.

---

## 📂 Project Structure
DOBI_UI/
│ best.pt # YOLO model weights
│ main.py # Streamlit UI entry point
│ run_bridge.sh # Script to start the ROS ↔ WebSocket bridge
│
├───assets/ # UI images, icons, etc.
├───bridge/
│ ros_node.py # ROS 2 node handling robot communication
│ server.py # WebSocket bridge server
│
├───camera/
│ camera_handler.py # Handles camera feed streaming
│
├───control/
│ auto_navigation.py # Autonomous navigation control
│ manual_control.py # Manual driving control
│
├───detection/
│ alert_logger.py # Logs detection alerts
│
└───utils/
config.py # Configuration parameters

---



## ⚙️ Installation

pip install streamlit opencv-python numpy websockets roslibpy
cd DOBI_UI
chmod +x run_bridge.sh
./run_bridge.sh
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
http://<raspberry_pi_ip>:8501



