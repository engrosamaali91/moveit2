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

Test moveit programatically

```bash 
ros2 run my_robot_commander_cpp test_moveit 
```


Create node and convert test_moveit file to Commander class

```bash
ros2 run my_robot_commander_cpp commander
```

in a seperate terminal check ```/open_gripper``` topic is a subscriber now with message type example_interfaces/msg/Bool


```bash
ros2 topic pub -1 /open_gripper example_interfaces/msg/Bool "{data: true}"
```

And observe if the gripper is being opened or closed


Now try to subscribe on topic ```joint_command``` to move the robot to the target pose, simply add a call back just like we did for gripper 

```bash 
ros2 topic pub -1 /joint_command example_interfaces/msg/Float64MultiArray "{data: [-0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}"
```


# Subscribe on Custom message 

```bash
ros2 topic pub -1 /pose_command my_robot_interfaces/msg/PoseCommand "{x: 0.7, y: 0.0, z: 0.2 ,roll: 3.14, pitch: 0.0, yaw: 0.0, cartesian_path: true}"
```







----------------------------------------------------------------------------------------

# Issues Encountered 

* The build failed for pacakge ```my_robot_commander_cpp``` because the MoveIt2 header name differed in ROS 2 Humble (.h instead of .hpp). Updating the include resolved the issue.