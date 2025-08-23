# midas
make sure you have the moveit binaries installed. 
all you need is 
`sudo apt install ros-humble-moveit`

Install dependencies for Ignition Gazebo

`sudo apt install ros-humble-ros-gz`

`sudo apt install ros-humble-ign-ros2-control`

build the packages with 
`colcon build`

source the install
`source install/setup.bash`

launch ignition gazebo first
`ros2 launch simple_moveit ign_gz.launch.py`

launch the demo
`ros2 launch simple_moveit demo.launch.py`

use sim time :

`ros2 param set /rviz use_sim_time true`

`ros2 param set /move_group use_sim_time true`

add the motion planner topic to rviz using the add button found on the bottom
- the interactive marker is missing. to manipulate joints you will have to slide them in joints tab
- any movement to J3 that causes it to collide with base at any point will result in planning and execution failure
- hit reset on bottom left after each execute
**