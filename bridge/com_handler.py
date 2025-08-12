# bridge/comm_handler.py
import time
from utils.config import CONTROL_MODE, SERIAL_PORT, BAUD_RATE, COMMAND_MAP
from threading import Lock

# Optional serial import
try:
    import serial
except Exception:
    serial = None

from .ros_node import RosNodeHandler

class SerialHandler:
    def __init__(self, port, baud):
        self._port = port
        self._baud = baud
        self._ser = None
        self._lock = Lock()
        if serial is None:
            print("[SerialHandler] pyserial not installed")
            return
        try:
            self._ser = serial.Serial(self._port, self._baud, timeout=0.1)
            print(f"[SerialHandler] opened {self._port} @ {self._baud}")
        except Exception as e:
            print("[SerialHandler] open failed:", e)
            self._ser = None

    def write(self, s):
        if self._ser is None:
            return False
        try:
            payload = s
            if isinstance(payload, str):
                # send newline terminated (ESP code reads single chars, newline is okay)
                b = (payload).encode()
            else:
                b = payload
            with self._lock:
                self._ser.write(b)
            return True
        except Exception as e:
            print("[SerialHandler] write error:", e)
            return False

    def read_latest(self):
        if self._ser is None:
            return None
        try:
            with self._lock:
                if self._ser.in_waiting:
                    return self._ser.readline().decode(errors='ignore').strip()
        except Exception as e:
            print("[SerialHandler] read error:", e)
        return None

    def close(self):
        try:
            if self._ser:
                self._ser.close()
        except:
            pass

class CommHandler:
    def __init__(self):
        self.ros = None
        self.serial = None
        self._lock = Lock()

        if CONTROL_MODE in ("ros", "both"):
            try:
                self.ros = RosNodeHandler()
                print("[CommHandler] ROS handler initialized")
            except Exception as e:
                print("[CommHandler] ROS init failed:", e)
                self.ros = None

        if CONTROL_MODE in ("serial", "both"):
            self.serial = SerialHandler(SERIAL_PORT, BAUD_RATE)

    def _map(self, cmd):
        if isinstance(COMMAND_MAP, dict):
            return COMMAND_MAP.get(cmd, cmd)
        return cmd

    def publish_command(self, logical_cmd):
        """
        logical_cmd: e.g. "forward", "left"
        """
        mapped = self._map(logical_cmd)
        # If mapped is multi-char, take first char for compatibility.
        if isinstance(mapped, str) and len(mapped) > 1:
            mapped_payload = mapped[0]
        else:
            mapped_payload = mapped

        # ROS path (publish std_msgs/Char)
        if self.ros:
            try:
                # publish the single char as ROS Char message
                self.ros.publish_command(mapped_payload)
            except Exception as e:
                print("[CommHandler] ros publish failed:", e)

        # Serial fallback
        if self.serial:
            try:
                # Write char (no newline needed; but allowed)
                self.serial.write(mapped_payload)
            except Exception as e:
                print("[CommHandler] serial write failed:", e)

    def publish_mode(self, mode_str):
        # Publish mode string to ROS (and serial as fallback)
        if self.ros:
            try:
                self.ros.publish_mode(mode_str)
            except Exception as e:
                print("[CommHandler] ros publish_mode failed:", e)
        if self.serial:
            try:
                # serial mode switch protocol is project dependent — many setups ignore it
                self.serial.write(mode_str + "\n")
            except Exception as e:
                print("[CommHandler] serial write mode failed:", e)

    def get_latest_data(self):
        # Prefer ROS telemetry
        if self.ros:
            try:
                d = self.ros.get_latest_data()
                if d is not None:
                    return d
            except Exception as e:
                print("[CommHandler] get_latest_data ros error:", e)
        # Fall back to serial reads
        if self.serial:
            return self.serial.read_latest()
        return None

    def close(self):
        if self.ros:
            try:
                self.ros.shutdown()
            except:
                pass
        if self.serial:
            try:
                self.serial.close()
            except:
                pass
