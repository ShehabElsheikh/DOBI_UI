#!/bin/bash
set -e
# Run the bridge server (ROS <-> WebSocket)

# Source ROS 2 environment (adjust if using different ROS installation)
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
fi

# If you have a colcon workspace for micro-ROS or local workspace, source it:
if [ -f "$HOME/ros2_ws/install/setup.bash" ]; then
    source "$HOME/ros2_ws/install/setup.bash"
fi

# Run bridge
python3 -m bridge.server
