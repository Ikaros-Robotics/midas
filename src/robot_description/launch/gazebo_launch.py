from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command, LaunchConfiguration 
from launch_ros.parameter_descriptions import ParameterValue
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Package paths
    pkg_share = get_package_share_directory('robot_description')
    
    # Path to your SDF model
    robot_sdf = os.path.join(pkg_share, 'urdf', 'robot.urdf')
    
    # World file
    default_world = os.path.join(pkg_share, 'world', 'empty_world.sdf')
    
    # Launch arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World file to load'
    )

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['ign sdf -p ', robot_sdf]),  # Convert SDF to URDF
                value_type=str
            ),
            'use_sim_time': True
        }],
        output='screen'
    )

    # Joint State Publisher (GUI)
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # Gazebo Sim
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': ['-r -v 4 ', LaunchConfiguration('world')],
            'on_exit_shutdown': 'true'
        }.items()
    )

    # Spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', robot_sdf,  # Use SDF directly
            '-name', 'midas',
            '-allow_renaming', 'true'
        ],
        output='screen'
    )

    # ROS 2 Control
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller',
             '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state',
             'active', 'joint_trajectory_controller'],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        gz_sim,
        spawn_robot,
        #load_joint_state_broadcaster,
        #load_joint_trajectory_controller,
    ])
