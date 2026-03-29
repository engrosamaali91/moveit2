# ROS 2 Workspace for Robot Arm

This repository contains a ROS 2 Humble workspace for a custom robot arm with:

- Robot description and RViz visualization
- ros2_control controllers
- MoveIt 2 configuration
- C++ commander nodes
- Custom message interfaces

All commands below are intended to be run from:

```bash
cd ~/moveit2_ws
```

## Prerequisites

Install required ROS 2 packages:

```bash
sudo apt update
sudo apt install -y \
  ros-humble-ros2-control \
  ros-humble-controller-manager \
  ros-humble-ros2-controllers
```

## Build the Workspace

```bash
# Pull latest changes (optional)
git pull origin main

# Build
colcon build

# Source overlay
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Important: run `source install/setup.bash` in every new terminal.

## Visualize the Robot in RViz

Use one of the following options.

```bash
# Option A: urdf_tutorial launcher
ros2 launch urdf_tutorial display.launch.py model:=/home/osama/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro

# Option B: package-specific launcher
ros2 launch my_robot_description display.launch.xml
```

## Launch MoveIt

```bash
ros2 launch my_robot_moveit_config demo.launch.py
```

## Bringup (Manual Multi-Terminal)

### Terminal 1: robot_state_publisher

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -p robot_description:="$(xacro ~/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro)"
```

### Terminal 2: ros2_control and controllers

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run controller_manager ros2_control_node --ros-args \
  -p robot_description:="$(xacro ~/moveit2_ws/src/my_robot_description/urdf/arm2arm.urdf.xacro)" \
  --params-file ~/moveit2_ws/src/my_robot_bringup/config/ros2_controllers.yaml
```

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner arm_controller
ros2 run controller_manager spawner gripper_controller

ros2 launch my_robot_moveit_config move_group.launch.py
```

### Terminal 3: RViz

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run rviz2 rviz2 -d ~/moveit2_ws/src/my_robot_description/rviz/urdf_config.rviz
```

Planning note: in RViz Motion Planning panel, select the desired planner plugin (for example, OMPL instead of CHOMP) based on your setup.

## Bringup (Single Launch File)

If you are using your combined bringup launch file:

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 launch my_robot_bringup my_robot.launch.xml
```

## Run Commander Nodes

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run my_robot_commander_cpp test_moveit
```

```bash
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

ros2 run my_robot_commander_cpp commander
```

## Topic-Based Functional Tests

### Gripper command

Confirm `/open_gripper` has a subscriber, then publish:

```bash
ros2 topic pub -1 /open_gripper example_interfaces/msg/Bool "{data: true}"
```

### Joint command

```bash
ros2 topic pub -1 /joint_command example_interfaces/msg/Float64MultiArray "{data: [-0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}"
```

### Custom pose command

```bash
ros2 topic pub -1 /pose_command my_robot_interfaces/msg/PoseCommand "{x: 0.7, y: 0.0, z: 0.2, roll: 3.14, pitch: 0.0, yaw: 0.0, cartesian_path: true}"
```

## Troubleshooting

### Error: `The passed message type is invalid`

Cause: terminal is not sourced with the local workspace overlay.

Fix:

```bash
cd ~/moveit2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 interface show my_robot_interfaces/msg/PoseCommand
```

If `ros2 interface show` succeeds, retry the publish command.

### Error: CMake source directory does not exist

Cause: stale CMake cache from an older package path.

Fix:

```bash
cd ~/moveit2_ws
rm -rf build/my_robot_interfaces install/my_robot_interfaces log/latest_build/my_robot_interfaces
colcon build --packages-select my_robot_interfaces --cmake-clean-cache
```

### Known build issue resolved

`my_robot_commander_cpp` initially failed to build because MoveIt 2 header naming in ROS 2 Humble used `.h` instead of `.hpp` for the referenced include. Updating the include resolved the issue.