from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler
from launch.substitutions import LaunchConfiguration, Command
from launch.event_handlers import OnProcessStart
import xacro
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()
    
    robot_description_file = os.path.join(
        get_package_share_directory('simple_moveit'),'config', 'robot_description.urdf.xacro'
    )
    
    joint_controllers_file = os.path.join(
        get_package_share_directory('simple_moveit'), 'config', 'moveit_controllers.yaml'
    )

    gazebo_launch_file = os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
    )

    robot_description = Command(['xacro ', robot_description_file])

    moveit_config = (
            MoveItConfigsBuilder("robot_description", package_name="simple_moveit")
        .robot_description_semantic(file_path = "config/robot_description.srdf")
        .robot_description(file_path = "config/robot_description.urdf.xacro")
        .trajectory_execution(file_path = "config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl","chomp"])
        .robot_description_kinematics(file_path = "config/kinematics.yaml")
        .to_moveit_configs()
                    )


    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments = {
        'use_sim_time': 'true',
            'debug': 'true',
            'gui': 'true',
            'paused': 'false',
            'world': [get_package_share_directory('simple_moveit'), 'worlds','grav_world.world']
        }.items()
    )

    rviz_config_path = os.path.join(
        get_package_share_directory('simple_moveit'),
        'config',
        'moveit.rviz'
    )

    rviz_node = Node(
        package = 'rviz2',
        executable = 'rviz2',
        name = 'rviz2',
        output = 'screen',
        arguments = ['-d', rviz_config_path],
        parameters = [
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
        ],

    )               

    robot_spawner_gazebo = Node(
        package = 'gazebo_ros',
        executable = 'spawn_entity.py',
        arguments = [
            '-entity', 'robot_description',
            '-topic', 'robot_description',
        ],
        output = 'screen',
    )

    ros_2_controllers_path = os.path.join(
                                get_package_share_directory("simple_moveit"),
                                                            "config",
                                                            "ros2_controllers.yaml",
                                )

    controller_manager_node = Node(
                                package = "controller_manager",
                                executable = "ros2_control_node",
                                parameters = [moveit_config.robot_description, joint_controllers_file],
                                output = "screen",
        remappings = [("~/robot_description", "/robot_description"),]
        
                                )
    
    joint_state_broadcaster_spawner = Node(
        package = "controller_manager",
        executable = "spawner",
        arguments = ["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output = "screen",
    )

    arm_controller_spawner = Node(
        package = "controller_manager",
        executable = "spawner",
        arguments = ["arm_planner_controller", "--controller-manager", "/controller_manager"],
        output = "screen",
    )

    use_sim_time = {"use_sim_time": True}
    config_dict = moveit_config.to_dict()
    config_dict.update(use_sim_time)


    move_group_node = Node(
        package = "moveit_ros_move_group",
        executable = "move_group",
        output = "screen",
        parameters = [config_dict],
        arguments = ["--ros-args", "--log-level", 'info'],
        )

    robot_state_publisher_node = Node(
        package = "robot_state_publisher",
        executable = "robot_state_publisher",
        output = "screen",
        parameters = [moveit_config.robot_description],

    )

    delay_joint_state_broadcaster = RegisterEventHandler(
        OnProcessStart(
            target_action = controller_manager_node,
            on_start = [joint_state_broadcaster_spawner],
        )
    )

    delay_arm_controller = RegisterEventHandler(
        OnProcessStart(
            target_action = joint_state_broadcaster_spawner,
            on_start = [arm_controller_spawner],
        )
    )

    delay_rviz_node = RegisterEventHandler(
        OnProcessStart(
            target_action = robot_state_publisher_node,
            on_start = [rviz_node],
        )
    )

    ld.add_action(gazebo)
    ld.add_action(controller_manager_node)
    ld.add_action(robot_spawner_gazebo)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(move_group_node)
    ld.add_action(delay_joint_state_broadcaster)
    ld.add_action(delay_arm_controller)
    ld.add_action(delay_rviz_node)

    return ld
