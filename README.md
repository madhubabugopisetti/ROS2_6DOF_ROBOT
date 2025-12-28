# ROS2_6DOF_ROBOT

## Installation
- ROS2 JAZZY: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
- GAZEBO HARMONIC: https://gazebosim.org/docs/harmonic/install_ubuntu
- ROS–Gazebo bridge: ``` sudo apt install ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz ```
- OTHERS: ``` sudo apt install python3-colcon-common-extensions ros-jazzy-joint-state-publisher ros-jazzy-joint-state-publisher-gui ```
- CHECKING: ``` sudo apt install liburdfdom-tools ```

## BUILD
```
cd ~/ros2_6dof_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

# GOAL 1: Render World in Gazebo

## STEP 1: Creating a workspace
```
mkdir -p ~/ros2_6dof_ws/src
cd ~/ros2_6dof_ws/src
source /opt/ros/jazzy/setup.bash
ros2 pkg create robot_description --build-type ament_cmake
```
## STEP 2: Create an empty world
* Create a folder worlds with file world.sdf<br />
* Add worlds to CMakeLists.txt<br />
* add a .gitignore<br />
* gz sim world.sdf<br />
## STEP 3: Launch Gazebo with ros2
- Create a folder launch with file world.launch.sdf<br />
- Add launch to CMakeLists.txt<br />
- [BUILD](#build)<br />
- ros2 launch robot_description world.launch.py<br />

# GOAL 2: Render 3DModel in Gazebo
## STEP 1:
- Our Model will have
```
shoulder_link
upper_arm_link
forearm_link
wrist_link
gripper_base
left_finger
right_finger
```
- Create a new folder meshes and move your dae files into this
- Create a new folder urdf with robot_arm.xacro
- Add meshes, urdf in CMakeLists.txt
- Add these in package.xml
```
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>joint_state_publisher</exec_depend>
<exec_depend>xacro</exec_depend>
<exec_depend>ros_gz_sim</exec_depend>
<exec_depend>ros_gz_bridge</exec_depend>
<exec_depend>gazebo_ros</exec_depend>
```
- Create a new file with arm_gazebo.launch.py in launch folder
- [BUILD](#build)
- ros2 launch robot_description arm_gazebo.launch.py