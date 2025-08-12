# main.py
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from camera.camera_handler import start_camera, stop_camera, get_latest_frame
from detection.alert_logger import log_detection, get_recent_alerts, clear_alerts
import json
import threading
import time

try:
    import websocket
except Exception:
    websocket = None

# === CONFIG ===
WS_URL = "ws://localhost:8000/ws"

# === WebSocket client wrapper ===
class WSClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.lock = threading.Lock()
        self.last_telemetry = None
        self._stop = False
        self._thread = None
        self._connect()

    def _connect(self):
        if websocket is None:
            print("websocket-client not installed")
            return
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.url, timeout=3)
            # start listener thread
            self._thread = threading.Thread(target=self._recv_loop, daemon=True)
            self._thread.start()
        except Exception as e:
            print("WS connect failed:", e)
            self.ws = None

    def _recv_loop(self):
        while not self._stop and self.ws:
            try:
                txt = self.ws.recv()
                if txt:
                    obj = json.loads(txt)
                    if obj.get("type") == "telemetry":
                        self.last_telemetry = obj.get("data")
            except Exception:
                time.sleep(0.1)

    def send(self, payload: dict):
        if not self.ws:
            return False
        try:
            with self.lock:
                self.ws.send(json.dumps(payload))
            return True
        except Exception as e:
            print("WS send error:", e)
            return False

    def get_telemetry(self):
        return self.last_telemetry

    def close(self):
        self._stop = True
        try:
            if self.ws:
                self.ws.close()
        except:
            pass

# === Start WS client ===
ws_client = None
try:
    ws_client = WSClient(WS_URL)
except Exception as e:
    st.warning(f"Could not start WS client: {e}")
    ws_client = None

# === Page ===
st.set_page_config(layout="wide")
st.title("🤖 DOBI: Autonomous Inspection System")

# === STATE ===
if 'nav_mode' not in st.session_state:
    st.session_state.nav_mode = "manual"

# TOP BAR
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚗 Navigation Mode")
    nav_choice = st.radio("Choose Mode:", ["Manual", "Autonomous"], horizontal=True)
    if nav_choice.lower() != st.session_state.nav_mode:
        st.session_state.nav_mode = nav_choice.lower()
        # send mode to bridge
        if ws_client:
            ws_client.send({"type": "mode", "data": "auto" if st.session_state.nav_mode=="autonomous" else "manual"})

    if st.session_state.nav_mode == "manual":
        st.subheader("🎮 Manual Control")

        # Buttons that send logical commands to bridge
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("⬆️ Forward (W)"):
                if ws_client: ws_client.send({"type": "command", "data": "forward"})
        with c2:
            if st.button("⏸ Stop (X)"):
                if ws_client: ws_client.send({"type": "command", "data": "stop"})
        with c3:
            if st.button("⬇️ Back (S)"):
                if ws_client: ws_client.send({"type": "command", "data": "backward"})

        c4, c5 = st.columns(2)
        with c4:
            if st.button("⬅️ Left (A)"):
                if ws_client: ws_client.send({"type": "command", "data": "left"})
        with c5:
            if st.button("➡️ Right (D)"):
                if ws_client: ws_client.send({"type": "command", "data": "right"})

with col2:
    st.subheader("🎮 Camera Control")
    cam_col1, cam_col2 = st.columns(2)
    with cam_col1:
        if st.button("▶️ Start Camera"):
            start_camera(log_detection)
    with cam_col2:
        if st.button("⏹ Stop Camera"):
            stop_camera()

# LIVE CAMERA
st.subheader("📷 Live Feed with Detection")
frame = get_latest_frame()
if frame is not None:
    st.image(frame, channels="BGR", caption="Live Annotated Feed")
else:
    st.info("Camera not active. Click 'Start Camera' to begin.")

# SIDEBAR TELEMETRY & ALERTS
with st.sidebar:
    st.header("📡 Telemetry")
    telemetry = ws_client.get_telemetry() if ws_client else None
    if telemetry:
        ultra_l = telemetry.get("ultrasonic_left")
        ultra_r = telemetry.get("ultrasonic_right")
        imu = telemetry.get("imu")
        st.metric("Ultrasonic Left (cm)", f"{ultra_l}" if ultra_l is not None else "N/A")
        st.metric("Ultrasonic Right (cm)", f"{ultra_r}" if ultra_r is not None else "N/A")
        if imu:
            st.markdown("**IMU (orientation)**")
            st.write(imu.get("orientation"))
    else:
        st.markdown("_No telemetry yet_")

    st.header("🚨 Detection Alerts")
    if st.button("🧹 Clear Alerts"):
        clear_alerts()
    alerts = get_recent_alerts(10)
    if alerts:
        for alert in alerts:
            st.markdown(f"**[{alert['time']}]** `{alert['label'].upper()}` - *{alert['severity']}*")
    else:
        st.markdown("No alerts")

# AUTO-REFRESH the feed & telemetry
st_autorefresh(interval=1000, limit=None, key="feed-refresh")

# Footer
st.markdown("---")
st.caption("DOBI BETA | Streamlit UI integrated with ROS2 (micro-ROS on ESP)")
