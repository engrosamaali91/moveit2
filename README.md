## 🚀 Run the Robot Arm Display

To build and launch the robot arm in RViz, run the following commands from your workspace root:

```bash
# 1. Pull the latest changes
git pull origin main

# 2. Build your ROS 2 workspace
colcon build

# 3. Source the workspace
source install/setup.bash

# 4. Launch the robot arm display in RViz
ros2 launch urdf_tutorial display.launch.py model:=/home/osama/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro

or 
# Laucnh the robot arm with display.launch.xml file
ros2 launch my_robot_description display.launch.xml

