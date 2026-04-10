# ROS 2 Workspace for Robot Arm

Quick command guide for build, bringup, MoveIt, and tests.

## Table of Contents

- [ROS 2 Workspace for Robot Arm](#ros-2-workspace-for-robot-arm)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Build Workspace](#build-workspace)
  - [Visualize in RViz](#visualize-in-rviz)
  - [Launch MoveIt Demo](#launch-moveit-demo)
  - [Bringup (Manual Multi-Terminal)](#bringup-manual-multi-terminal)
    - [Terminal 1](#terminal-1)
    - [Terminal 2](#terminal-2)
    - [Terminal 3](#terminal-3)
  - [Bringup (Single Launch)](#bringup-single-launch)
  - [Run Commander Nodes](#run-commander-nodes)
    - [Topic Functional Tests](#topic-functional-tests)
  - [Troubleshooting](#troubleshooting)
  - [Interacti with moveit using c++ api](#interacti-with-moveit-using-c-api)
  - [interact with moveit using pythonapi](#interact-with-moveit-using-pythonapi)

## Prerequisites

Run from workspace root:

```bash
cd ~/moveit2_ws
```

Update apt index:

```bash
sudo apt update
```

Install required ROS 2 packages:

```bash
sudo apt install -y \
  ros-humble-ros2-control \
  ros-humble-controller-manager \
  ros-humble-ros2-controllers
```

## Build Workspace

Pull latest changes (optional):

```bash
git pull origin main
```

Build all packages:

```bash
colcon build
```

Source ROS 2 base environment:

```bash
source /opt/ros/humble/setup.bash
```

Source workspace overlay (run in every new terminal):

```bash
source install/setup.bash
```

## Visualize in RViz

Launch URDF via urdf_tutorial:

```bash
ros2 launch urdf_tutorial display.launch.py model:=/home/osama/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro
```

Launch package display file:

```bash
ros2 launch my_robot_description display.launch.xml
```

## Launch MoveIt Demo

Launch MoveIt demo setup:

```bash
ros2 launch my_robot_moveit_config demo.launch.py
```

## Bringup (Manual Multi-Terminal)

### Terminal 1

Source ROS 2 base environment:

```bash
source /opt/ros/humble/setup.bash
```

Source workspace overlay:

```bash
source ~/moveit2_ws/install/setup.bash
```

Start robot_state_publisher with xacro robot description:

```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -p robot_description:="$(xacro ~/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro)"
```

### Terminal 2

Source ROS 2 base environment:

```bash
source /opt/ros/humble/setup.bash
```

Source workspace overlay:

```bash
source ~/moveit2_ws/install/setup.bash
```

Start ros2_control node with controller config:

```bash
ros2 run controller_manager ros2_control_node --ros-args \
  -p robot_description:="$(xacro ~/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro)" \
  --params-file ~/moveit2_ws/src/my_robot_bringup/config/ros2_controllers.yaml
```

Spawn joint state broadcaster:

```bash
ros2 run controller_manager spawner joint_state_broadcaster
```

Spawn arm controller:

```bash
ros2 run controller_manager spawner arm_controller
```

Spawn gripper controller:

```bash
ros2 run controller_manager spawner gripper_controller
```

Launch MoveIt move_group:

```bash
ros2 launch my_robot_moveit_config move_group.launch.py
```

### Terminal 3

Source ROS 2 base environment:

```bash
source /opt/ros/humble/setup.bash
```

Source workspace overlay:

```bash
source ~/moveit2_ws/install/setup.bash
```

Open RViz with robot config:

```bash
ros2 run rviz2 rviz2 -d ~/moveit2_ws/src/my_robot_description/rviz/urdf_config.rviz
```

## Bringup (Single Launch)

Source ROS 2 base environment:

```bash
source /opt/ros/humble/setup.bash
```

Source workspace overlay:

```bash
source ~/moveit2_ws/install/setup.bash
```

Run combined bringup launch:

```bash
ros2 launch my_robot_bringup my_robot.launch.xml
```

## Run Commander Nodes

Source ROS 2 base environment:

```bash
source /opt/ros/humble/setup.bash
```

Source workspace overlay:

```bash
source ~/moveit2_ws/install/setup.bash
```

Run MoveIt C++ test node:

```bash
ros2 run my_robot_commander_cpp test_moveit
```

Run main commander node:

```bash
ros2 run my_robot_commander_cpp commander
```

### Topic Functional Tests

Publish open-gripper command once:

```bash
ros2 topic pub -1 /open_gripper example_interfaces/msg/Bool "{data: true}"
```

Publish joint target array once:

```bash
ros2 topic pub -1 /joint_command example_interfaces/msg/Float64MultiArray "{data: [-0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}"
```

Publish custom pose command once:

```bash
ros2 topic pub -1 /pose_command my_robot_interfaces/msg/PoseCommand "{x: 0.7, y: 0.0, z: 0.2, roll: 3.14, pitch: 0.0, yaw: 0.0, cartesian_path: true}"
```

## Troubleshooting

Fix invalid message type by re-sourcing and checking interface:

```bash
cd ~/moveit2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 interface show my_robot_interfaces/msg/PoseCommand
```

Fix stale CMake cache for my_robot_interfaces:

```bash
cd ~/moveit2_ws
rm -rf build/my_robot_interfaces install/my_robot_interfaces log/latest_build/my_robot_interfaces
colcon build --packages-select my_robot_interfaces --cmake-clean-cache
```

## Interacti with moveit using c++ api

Placeholder: add C++ MoveIt API examples and usage notes here.

## interact with moveit using pythonapi

Placeholder: add Python MoveIt API examples and usage notes here.