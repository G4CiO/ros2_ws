# import os

# from launch import LaunchDescription
# from launch_ros.actions import Node
# from ament_index_python.packages import get_package_share_directory

# from launch.actions import ExecuteProcess, DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration

# def generate_launch_description():

#     # define object of launch script
#     launch_description = LaunchDescription()
#     package_name = 'turtle_bringup'
#     executable_name = 'crazy_turtle.py'

# # -------------------------------------------------------------------------
#     name_turtle2_launch_arg = DeclareLaunchArgument(
#         'name_turtle2',
#         default_value='turtle2',  # Default to 'turtle2'
#         description='Name of the first turtle to spawn'
#     )
#     launch_description.add_action(name_turtle2_launch_arg)

#     name_turtle3_launch_arg = DeclareLaunchArgument(
#         'name_turtle3',
#         default_value='turtle3',  # Default to 'turtle3'
#         description='Name of the second turtle to spawn'
#     )
#     launch_description.add_action(name_turtle3_launch_arg)
# # -------------------------------------------------------------------------



#     # rviz config
#     rviz_config = os.path.join(
#         get_package_share_directory(package_name),
#         'rviz',
#         'fun2.rviz'
#     )

#     # Check if rviz config file exists
#     if not os.path.exists(rviz_config):
#         print(f"Error: RViz configuration file not found at {rviz_config}")
#         return launch_description

#     # run turtlesim_plus
#     turtlesim_node = Node(
#         package='turtlesim_plus',
#         executable='turtlesim_plus_node.py',
#         name='turtlesim'
#     )
#     launch_description.add_action(turtlesim_node)

#     # run rviz
#     rviz = Node(
#          package='rviz2',
#          executable='rviz2',
#          name='rviz2',
#          arguments=['-d', rviz_config],
#          output='screen'
#     )
#     launch_description.add_action(rviz)

# # -------------------------------------------------

#     # run controller
#     controller_node = Node(
#         package=package_name,
#         executable='controller.py',
#         name='controller'
#     )
#     launch_description.add_action(controller_node)

# # -------------------------------------------------------------------------

# # ต้อง call service spawn_turtle ตัวใหม่ ใน launch file ก่อน แล้วค่อยสร้าง namespace ใน crazy_turtle3 ขึ้นมาทำให้ไม่ต้องคอย remap
#     # run crazy_turtle2
#     crazy_turtle2 = Node(
#         package=package_name,
#         # namespace='turtle2',
#         executable=executable_name,
#         name='turtle2_crazy_turtle',
#         parameters=[{'name_turtle': LaunchConfiguration('name_turtle2')}]
#         )
#     launch_description.add_action(crazy_turtle2)
    
#     # Spawn turtle3 using a service call
#     x = 0.0
#     y = 11.0
#     theta = 0.0
#     name = 'turtle3'

#     spawn_turtle = ExecuteProcess(
#         cmd=[
#             'ros2', 'service', 'call',
#             '/spawn_turtle',
#             'turtlesim/srv/Spawn',
#             f'x: {x} y: {y} theta: {theta} name: "{name}"'
#         ],
#         output='screen',
#     )
#     launch_description.add_action(spawn_turtle)

#     # Run crazy_turtle3 node under its own namespace
#     crazy_turtle3 = Node(
#         package=package_name,
#         namespace='turtle3',  # Namespace for turtle3
#         executable=executable_name,
#         name='turtle3_crazy_turtle',
#         parameters=[{'name_turtle': LaunchConfiguration('name_turtle3')}]
#     )
#     launch_description.add_action(crazy_turtle3)

#     # crazy_turtle3 = Node(
#     #     package=package_name,
#     #     # namespace='turtle3',
#     #     executable=executable_name,
#     #     name='turtle3_crazy_turtle',
#     #     parameters=[{'name_turtle': LaunchConfiguration('name_turtle3')}],
#     #     remappings=[
#     #         ('/turtle2/pose', '/turtle3/pose'),
#     #         ('/turtle2/cmd_vel', '/turtle3/cmd_vel'),
#     #         ('/crazy_pizza', '/crazy_pizza3'),
#     #         ('/turtle2/eat', '/turtle3/eat' )
#     #     ]
#     #     )
#     # launch_description.add_action(crazy_turtle3)

#     # crazy_pizza3 = Node(
#     #     package=package_name,
#     #     executable='crazy_pizza.py',
#     #     name='crazy_pizza_publisher3',
#     #     remappings=[
#     #         ('/crazy_pizza', '/crazy_pizza3')
#     #     ]
#     # )
#     # launch_description.add_action(crazy_pizza3)

# # -------------------------------------------------------------------------


#     # run odom_publisher
#     odom = Node(
#         package=package_name,
#         executable='odom_publisher.py',
#         name='odom_publisher'
#     )
#     launch_description.add_action(odom)

#     # run crazy_pizza
#     crazy_pizza = Node(
#         package=package_name,
#         executable='crazy_pizza.py'
#     )
#     launch_description.add_action(crazy_pizza)

#     return launch_description

import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def spawn_turtle_service_call(x, y, theta, name):
    return ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/spawn_turtle',
            'turtlesim/srv/Spawn',
            f"'{{x: {x}, y: {y}, theta: {theta}, name: \"{name}\"}}'"
        ],
        shell=True,  # Use shell=True for formatted strings
        output='screen',
    )

def kill_turtle_service_call(name):
    return ExecuteProcess(
        cmd=[
            'ros2', 'service', 'call',
            '/remove_turtle',
            'turtlesim/srv/Kill',
            f"'{{name: \"{name}\"}}'"
        ],
        shell=True,  # Use shell=True for formatted strings
        output='screen',
    )


def generate_launch_description():

    # Define the launch description object
    launch_description = LaunchDescription()
    package_name = 'turtle_bringup'

    # RViz configuration
    # rviz_config = os.path.join(
    #     get_package_share_directory(package_name),
    #     'rviz',
    #     'fun2.rviz'
    # )

    rviz_config = os.path.join(
        os.getenv("HOME"), "ros2_ws", "src", "turtle_bringup", "rviz", "fun2.rviz"
    )

    # Check if RViz config file exists
    if not os.path.exists(rviz_config):
        print(f"Error: RViz configuration file not found at {rviz_config}")
        return launch_description
    
    # Run RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )
    # launch_description.add_action(rviz)
# --------------------------------------------------------------------------
    # Run turtlesim_plus node
    turtlesim_node = Node(
        package='turtlesim_plus',
        executable='turtlesim_plus_node.py',
        name='turtlesim'
    )
    launch_description.add_action(turtlesim_node)

    kill_turtle1 = kill_turtle_service_call('turtle1')
    launch_description.add_action(kill_turtle1)

    spawn_turtle1 = spawn_turtle_service_call(x=-5.0, y=-5.0, theta=3.14, name='V')
    launch_description.add_action(spawn_turtle1)

    # Run controller node
    controller_node = Node(
        package=package_name,
        namespace='V',
        executable='controller.py',
        name='controller',
        parameters=[
            {'frequency': 100.0}
        ]
    )
    launch_description.add_action(controller_node)

    # Spawn turtle2 using the function to create the service call
    spawn_turtle2 = spawn_turtle_service_call(x=7.5, y=5.5, theta=1.57, name='KAI')
    launch_description.add_action(spawn_turtle2)

    # Run crazy_turtle2 node
    crazy_turtle2 = Node(
        package=package_name,
        namespace='KAI',
        executable='crazy_turtle.py',
        name='crazy_turtle',
        parameters=[
            {'frequency': 100.0}
        ]
    )
    launch_description.add_action(crazy_turtle2)

    # Run crazy_pizza node
    crazy_pizza = Node(
        package=package_name,
        executable='crazy_pizza.py',
    )
    launch_description.add_action(crazy_pizza) #ห้ามเปิดคู่ odom
# --------------------------------------------------------------------------
    # Run odom_publisher node
    odom = Node(
        package=package_name,
        executable='odom_publisher.py',
        parameters=[
            {'nameturtle1': 'A'},
            {'nameturtle2': 'B'}
        ]
    )
    # launch_description.add_action(odom) #ห้ามเปิดคู่ crazy_pizza

    return launch_description
