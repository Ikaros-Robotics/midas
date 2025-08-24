#include "custom_paths.h"

#include "rclcpp/rclcpp.hpp"

#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

#include <moveit_msgs/msg/display_robot_state.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>


class custom_paths::CartesianPathsNode: public rclcpp::Node {

public:

    CartesianPathsNode();
    ~CartesianPathsNode();

    void start();

private:

    static const std::string PLANNING_GROUP_ARM = "ur_manipulator";

    moveit::planning_interface::MoveGroupInterface move_group_arm;

    void custom_paths::CartesianPathsNode::follow_path(const std::vector<geometry_msgs::msg::Pose>& waypoints);
    
    // std::vector<double> joint_group_positions_arm;


    
}