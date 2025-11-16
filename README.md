## 🚀 ROS 2 Workspace for Robot Arm

To build and run the project, execute the following commands from the workspace root (`~/moveit2_ws`).

```bash
# 1. Pull the latest changes
git pull origin main

# 2. Build your ROS 2 workspace
colcon build

# 3. Source the workspace
# (You must do this in every new terminal)
source install/setup.bash
```

### 🤖 Launch Robot Arm Display

To visualize the robot arm model in RViz, you can use either of the following commands:

```bash
# Option A: Using the generic urdf_tutorial launcher
ros2 launch urdf_tutorial display.launch.py model:=/home/osama/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro
# Option B: Using the package's specific launcher
ros2 launch my_robot_description display.launch.xml
```


### Launch moveit config package

prior to launch 
```bash
sudo apt install \
  ros-humble-ros2-control \
  ros-humble-controller-manager \
  ros-humble-ros2-controllers
```

```bash
ros2 launch my_robot_moveit_config demo.launch.py 
```