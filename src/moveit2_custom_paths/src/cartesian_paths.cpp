
#include "moveit2_custom_paths/cartesian_paths.h"



custom_paths::CartesianPathsNode::CartesianPathsNode(): Node("cartesian_paths_node"){

    this->move_group_arm(this, this->PLANNING_GROUP_ARM);

    this->path_sub = this->create_subscription<std::vector<geometry_msgs::msg::Pose>>("waypoints", 10, std::bind(&midas_controller::MidasControllerNode::follow_path, this, std::placeholders::_1));
}

custom_paths::CartesianPathsNode::~CartesianPathsNode(){}


void custom_paths::CartesianPathsNode::start(){

}

void custom_paths::CartesianPathsNode::follow_path(const std::vector<geometry_msgs::msg::Pose>& waypoints){
    const moveit::core::JointModelGroup *joint_model_group_arm = this->move_group_arm.getCurrentState()->getJointModelGroup(this->PLANNING_GROUP_ARM);

    // Get Current State
    moveit::core::RobotStatePtr current_state_arm =
    this->move_group_arm.getCurrentState(10);

    std::vector<double> joint_group_positions_arm;
    current_state_arm->copyJointGroupPositions(joint_model_group_arm,
                                            joint_group_positions_arm);

    this->move_group_arm.setStartStateToCurrentState();

    moveit_msgs::msg::RobotTrajectory trajectory_approach;
    const double jump_threshold = 0.0;
    const double eef_step = 0.01;

    double fraction = this->move_group_arm.computeCartesianPath(
        waypoints, eef_step, jump_threshold, trajectory_approach);

    this->move_group_arm.execute(trajectory_approach);

}