from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # create name node
    turtle_spawner = Node(
        package="turtlesim_catch_them_all",
        executable="turtle_spawner",
        # add parameter new value
        parameters=[
            {"timer": 0.8}
        ]
    )

    # create name node
    turtle_controller = Node(
        # name of directory
        package="turtlesim_catch_them_all",
        # name of executable
        executable="turtle_controller"
    )

    turtlesim = Node(
        # name of directory
        package="turtlesim",
        # name of executable
        executable="turtlesim_node"
    )
    
    # add to the launch description
    ld.add_action(turtle_controller)
    ld.add_action(turtle_spawner)
    ld.add_action(turtlesim)
    return ld