cmake_minimum_required(VERSION 3.5)
project(midas_interface)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(controller_manager REQUIRED)
find_package(rclcpp REQUIRED)
find_package(pluginlib REQUIRED)


add_library(midas_interface SHARED
src/midas_hw_interface.cpp)

target_link_libraries(midas_interface)

target_include_directories(
  midas_interface
  PRIVATE
  include
)
ament_target_dependencies(
  midas_interface
  hardware_interface
  controller_manager
  rclcpp
  pluginlib
)

pluginlib_export_plugin_description_file(hardware_interface robot_hardware.xml)


install(
  TARGETS midas_interface
  DESTINATION lib
)

install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}
)

ament_export_libraries(
  midas_interface
)
ament_export_dependencies(
  hardware_interface
  controller_manager
  rclcpp
  pluginlib
)


ament_package()