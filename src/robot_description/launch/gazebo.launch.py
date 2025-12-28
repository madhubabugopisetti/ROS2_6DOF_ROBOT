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

    world = os.path.join(pkg_robot, 'worlds', 'world.sdf')
    xacro = os.path.join(pkg_robot, 'urdf', 'robot_arm.xacro')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gz, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world}'}.items()
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', xacro]),
            'use_sim_time': True
        }]
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'robot_arm',
            '-topic', 'robot_description'
        ]
    )

    return LaunchDescription([gazebo, rsp, spawn])
