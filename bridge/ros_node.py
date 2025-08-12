# bridge/ros_node.py
import threading
import queue
import rclpy
from rclpy.node import Node
from std_msgs.msg import Char, String, Float32
from sensor_msgs.msg import Imu

class DobbiRosNode(Node):
    def __init__(self):
        super().__init__('dobbi_bridge_node')
        # Publishers
        self.cmd_pub = self.create_publisher(Char, '/motor_command', 10)
        self.mode_pub = self.create_publisher(String, '/control_mode', 10)

        # Telemetry subscriptions
        self.ultra_left = None
        self.ultra_right = None
        self.imu_data = None

        self._lock = threading.Lock()

        self.create_subscription(Float32, '/ultrasonic_left', self._ultra_left_cb, 10)
        self.create_subscription(Float32, '/ultrasonic_right', self._ultra_right_cb, 10)
        self.create_subscription(Imu, '/imu', self._imu_cb, 10)

    def _ultra_left_cb(self, msg: Float32):
        with self._lock:
            self.ultra_left = float(msg.data)

    def _ultra_right_cb(self, msg: Float32):
        with self._lock:
            self.ultra_right = float(msg.data)

    def _imu_cb(self, msg: Imu):
        # convert to a compact dict summary
        with self._lock:
            self.imu_data = {
                "orientation": {
                    "x": msg.orientation.x,
                    "y": msg.orientation.y,
                    "z": msg.orientation.z,
                    "w": msg.orientation.w
                },
                "angular_velocity": {
                    "x": msg.angular_velocity.x,
                    "y": msg.angular_velocity.y,
                    "z": msg.angular_velocity.z
                },
                "linear_acceleration": {
                    "x": msg.linear_acceleration.x,
                    "y": msg.linear_acceleration.y,
                    "z": msg.linear_acceleration.z
                }
            }

    def publish_command(self, char_payload: str):
        """
        Publish a single-character command to /motor_command as std_msgs/Char.
        Accepts either a 1-char string or an int.
        """
        m = Char()
        if isinstance(char_payload, str):
            if len(char_payload) == 0:
                return
            # Char message expects an integer 0-255
            m.data = ord(char_payload[0])
        elif isinstance(char_payload, (int,)):
            m.data = char_payload
        else:
            # fallback: encode first char
            m.data = ord(str(char_payload)[0])
        self.cmd_pub.publish(m)

    def publish_mode(self, mode_str: str):
        m = String()
        m.data = str(mode_str)
        self.mode_pub.publish(m)

    def get_latest_telemetry(self):
        with self._lock:
            return {
                "ultrasonic_left": self.ultra_left,
                "ultrasonic_right": self.ultra_right,
                "imu": self.imu_data
            }

# Helper class to run rclpy in background and expose the node
class RosNodeHandler:
    def __init__(self):
        rclpy.init(args=None)
        self.node = DobbiRosNode()
        self._spin_thread = threading.Thread(target=self._spin, daemon=True)
        self._running = True
        self._spin_thread.start()

    def _spin(self):
        try:
            while self._running and rclpy.ok():
                rclpy.spin_once(self.node, timeout_sec=0.01)
        except Exception as e:
            print("[RosNodeHandler] spin error:", e)

    def publish_command(self, mapped_char):
        try:
            self.node.publish_command(mapped_char)
        except Exception as e:
            print("[RosNodeHandler] publish_command error:", e)

    def publish_mode(self, mode_str):
        try:
            self.node.publish_mode(mode_str)
        except Exception as e:
            print("[RosNodeHandler] publish_mode error:", e)

    def get_latest_data(self):
        return self.node.get_latest_telemetry()

    def shutdown(self):
        self._running = False
        # Allow spin thread to stop
        try:
            rclpy.shutdown()
        except:
            pass
