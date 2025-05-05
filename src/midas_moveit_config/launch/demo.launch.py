import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    launch_arguments = {
        "robot_ip": "xxx.yyy.zzz.www",
        "use_fake_hardware": "true",
        "dof": "6",
    }


    moveit_config = (
            MoveItConfigsBuilder("midas", package_name="midas_moveit_config")

            .robot_description(mappings=launch_arguments)
    
            .trajectory_execution(file_path="config/moveit_controllers.yaml")
    
            .planning_scene_monitor(
            publish_robot_description=True,publish_robot_description_semantic=True)
    
            .planning_pipelines(pipelines=["ompl"])
    
            .to_moveit_configs()
        )


    move_group_node = Node(
            package = ("moveit_ros_move_group"),
            executable = "move_group",
            output = "screen",
            parameters=[moveit_config.to_dict()],
            )


    # RViz for visualization
    # Get the path to the RViz configuration file
    rviz_config_arg = DeclareLaunchArgument(
        "rviz_config",
        default_value="midas_moveit_demo.rviz",
        description="RViz configuration file",
    )
    rviz_base = LaunchConfiguration("rviz_config")

    # Launch RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
        ],
    )

    # Static TF
    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["--frame-id", "world", "--child-frame-id", "base_link"],
    )

    # Publish TF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
    )

    # ros2_control using mock hardware for trajectory execution
    ros2_controllers_path = os.path.join(
        get_package_share_directory("midas_moveit_config"),
        "config",
        "ros2_controllers.yaml",
    )
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[ros2_controllers_path],
        remappings=[
            ("/controller_manager/robot_description", "/robot_description"),
        ],
        output="both",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller", "-c", "/controller_manager"],
        )

    return LaunchDescription(
        [
            rviz_config_arg,
            rviz_node,
            static_tf,
            robot_state_publisher,
            move_group_node,
            ros2_control_node,
            joint_state_broadcaster_spawner,
            arm_controller_spawner,

        ]
        )

