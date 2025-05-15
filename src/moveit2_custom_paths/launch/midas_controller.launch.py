import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    midas_node = Node(
        name="midas_controller_node",
        package="moveit2_custom_paths",
        executable="midas_controller_node",
        output="screen",
        remappings=[
            ('joint_states', '/joint_states'),
        ],
    )

    return LaunchDescription(
        [midas_node]
    )