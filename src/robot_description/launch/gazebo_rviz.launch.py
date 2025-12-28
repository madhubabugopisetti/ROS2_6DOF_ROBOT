import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():
    pkg_robot = get_package_share_directory('robot_description')
    pkg_gz = get_package_share_directory('ros_gz_sim')

    world_file = os.path.join(pkg_robot, 'worlds', 'world.sdf')
    xacro_file = os.path.join(pkg_robot, 'urdf', 'robot_arm.xacro')
    rviz_config = os.path.join(pkg_robot, 'config', 'rviz.rviz')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gz, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    joint_state_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model'],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', xacro_file]),
            'use_sim_time': True
        }]
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'robot_arm', '-topic', 'robot_description'],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        clock_bridge,
        joint_state_bridge,
        robot_state_publisher,
        spawn_entity,
        rviz
    ])
