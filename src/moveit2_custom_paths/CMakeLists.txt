cmake_minimum_required(VERSION 3.8)
project(moveit2_custom_paths)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(moveit_core REQUIRED)
find_package(moveit_ros_planning REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(interactive_markers REQUIRED)
find_package(geometric_shapes REQUIRED)
find_package(control_msgs REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)


rosidl_generate_interfaces(${PROJECT_NAME}
      "srv/ResetJointStates.srv" 
      DEPENDENCIES    
)

rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

include_directories(include)
include_directories(SYSTEM)
include_directories(${rosidl_default_runtime_INCLUDE_DIRS})
# add_executable(cartesian_paths src/cartesian_paths.cpp)
# target_include_directories(cartesian_paths PUBLIC
#   $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
#   $<INSTALL_INTERFACE:include>)
# target_compile_features(cartesian_paths PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

# install(TARGETS cartesian_paths
#   DESTINATION lib/${PROJECT_NAME})



add_executable(midas_controller_node src/midas_controller_node.cpp src/midas_controller.cpp)
target_include_directories(midas_controller_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_link_libraries(midas_controller_node ${cpp_typesupport_target})
target_compile_features(midas_controller_node PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

# install(TARGETS midas_controller_node
#   DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# ament_target_dependencies(cartesian_paths
#     ament_cmake
# 	rclcpp
# 	rclcpp_action
# 	moveit_core
# 	moveit_ros_planning_interface
# 	interactive_markers
# 	moveit_ros_planning
# 	control_msgs)

#   # Install the executable
# install(TARGETS 
# cartesian_paths
#   DESTINATION lib/${PROJECT_NAME}
# )

ament_target_dependencies(midas_controller_node
    ament_cmake
    rclcpp
    rclcpp_action
    sensor_msgs
    moveit_core
    moveit_ros_planning_interface
    interactive_markers
    moveit_ros_planning
    control_msgs)

    

  # Install the executable
install(TARGETS 
midas_controller_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install the launch file
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)


ament_package()
