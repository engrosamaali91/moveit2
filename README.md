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




### Run from terminal robot bringup package

```bash 
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro /home/osama/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro)"
```

in a seperate terminal 
```bash
# In a clean terminal
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run controller_manager ros2_control_node --ros-args \
  -p robot_description:="$(xacro ~/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro)" \
  --params-file ~/moveit2_ws/src/my_robot_bringup/config/ros2_controllers.yaml
```

```bash
ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner arm_controller
ros2 run controller_manager spawner gripper_controller

ros2 launch my_robot_moveit_config move_group.launch.py
```

In a seperate terminal
```bash
ros2 run rviz2 rviz2 -d ~/moveit2_ws/src/my_robot_description/rviz/urdf_config.rviz 
```

> Note: Go to context and add motionPlanner and then change CHOMP to ompl


After that i created my_robot_bringup launch file that launches all the above nodes

```bash 
ros2 launch my_robot_bringup my_robot.launch.xml
```