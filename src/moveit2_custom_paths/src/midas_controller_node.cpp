
#include "moveit2_custom_paths/midas_controller.h"


int main(int argc, char** argv) {

  rclcpp::init(argc, argv);
  auto node = std::make_shared<midas_controller::MidasControllerNode>();
  rclcpp::executors::MultiThreadedExecutor executor;
  executor.add_node(node);
  executor.spin();

  rclcpp::shutdown();

  return 0;

}