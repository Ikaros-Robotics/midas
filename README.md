# midas
make sure you have the moveit binaries installed. 
all you need is 
`sudo apt install ros-humble-moveit`


build the packages with colcon build

source the install
`source install/setup.bash`

launch the demo
`ros2 launch midas_moveit_config`

add the motion planner topic to rviz using the add button found on the bottom
- the interactive marker is missing. to manipulate joints you will have to slide them in joints tab
- any movement to J3 that causes it to collide with base at any point will result in planning and execution failure
- hit reset on bottom left after each exectute
