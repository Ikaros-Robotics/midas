// #include "dlio/map.h"

#include "moveit2_custom_paths/cartesian_paths.h"

int main(int argc, char** argv) {

  rclcpp::init(argc, argv);
  auto node = std::make_shared<custom_paths::CartesianPathsNode>();
  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();

  return 0;

}