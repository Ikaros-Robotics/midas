from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.actions import SetParameter
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("robot_description", package_name="simple_moveit").to_moveit_configs()

    robot_description_pkg = get_package_share_directory('simple_moveit')
    xacro_file = os.path.join(robot_description_pkg, 'config', 'robot_description.urdf.xacro')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    return LaunchDescription([
        
        SetParameter(name='use_sim_time', value=True),

        # Launch Ignition Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
            ]),
            launch_arguments={
                'gz_args': '-r empty.sdf'  # Launch empty world
            }.items()
        ),

        # Spawn robot in Ignition Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-name', 'midas', '-x', '0', '-y', '0', '-z', '0.1',
                       '-topic', 'robot_description'],
            output='screen'
        ),

        # Publish robot description to /robot_description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        generate_demo_launch(moveit_config),
    ])
