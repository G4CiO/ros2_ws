from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # run turtlesim_plus_node
        Node(
            package='turtlesim_plus',
            executable='turtlesim_plus_node.py',
            name='turtlesim' # name node
        ),
        # run noise_generator(namespace = linear)
        Node(
            package='lab1',
            namespace='linear',
            executable='noise_generator.py',
            name='linear_noise'
        ),
        # run noise_generator(namespace = angular)
        Node(
            package='lab1',
            namespace='angular',
            executable='noise_generator.py',
            name='angular_noise'
        ),
        # run velocity_mux
        Node(
            package='lab1',
            executable='velocity_mux.py',
            name='mux',
            remappings=[
                ('/cmd_vel', '/turtle1/cmd_vel') # change topic name (old,new)
            ]
        )
    ])