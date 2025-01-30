from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# for Call service from Launch file
def generate_launch_description():

    # define object of launch script
    launch_description = LaunchDescription()

    interface_type = "my_robot_interfaces/srv/SetNoise"
    # create ExecuteProcess
    noise_propeties = [
        ('/linear', 10.0, 1.0), # (namespace, mean_value, variance_value)
        ('/angular', 0.0, 3.0)
    ]

    for ns, mean, var in noise_propeties:
        set_noise = ExecuteProcess(
            # มาจาก command line ตอน ros2 service call
            # cmd=[[
            #     'ros2 service call ',
            #     str(ns),
            #     '/set_noise ',
            #     interface_type,
            #     ' ',
            #     f'"{{
            #         mean: {{data: {mean}}},
            #         variance: {{data: {var}}}
            #         }}"'
            # ]],
            # shell=True

            # cmd=['ros2', 'service', 'call', '/linear/set_noise', 'my_robot_interfaces/srv/SetNoise', '{"mean": {"data": 1.0}, "variance": {"data": 0.1}}'],
            # output='screen',

            cmd=[
                'ros2', 'service', 'call',
                f'{ns}/set_noise', interface_type,
                f"{{mean: {{data: {mean}}}, variance: {{data: {var}}}}}"
            ],
            output='screen'
        )
        launch_description.add_action( set_noise )

    return launch_description