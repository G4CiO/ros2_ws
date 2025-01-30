from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    # define object of launch script
    launch_description = LaunchDescription()

    # ประกาศ LaunchConfig เพื่อให้ Launch file อื่นๆ สามารถปรับ parameter Launch file นี้ได้ (concept คล้ายๆ ros param)
    rate_mux = LaunchConfiguration('rate')
    rate_launch_arg = DeclareLaunchArgument(
        'rate',
        default_value='5.0' # ใส่เพื่อ ถ้าปกติเราไม่ได้ประกาศ rate ก็จะดึงค่า default ไปใช้แทน
    )
    # ใส่ action ของ rate_launch_arg ตอน launch file นี้
    launch_description.add_action(rate_launch_arg)

    # run turtlesim_plus
    turtlesim_node = Node(
        package='turtlesim_plus',
        executable='turtlesim_plus_node.py',
        name='turtlesim'
    )
    launch_description.add_action(turtlesim_node)

    # create 2 node------------------------------------------
    package_name = 'lab1'
    executable_noise = 'noise_generator.py'
    namespace = ['linear', 'angular']
    rate = [10.0, 30.0]
    for i in range(len(namespace)):
        # create noise_generator_node for 2 namespace
        noise_gen = Node(
            package=package_name,
            namespace=namespace[i],
            executable=executable_noise,
            name=namespace[i] + '_noise',
            parameters=[
                {'rate':rate[i] }
            ]
        )
        launch_description.add_action(noise_gen)

        # run velocity_mux
        vero_mux = Node(
            package=package_name,
            executable='velocity_mux.py',
            name='mux',
            remappings=[
                ('/cmd_vel', '/turtle1/cmd_vel') # change topic name (old,new)
            ],
            parameters=[
                {'rate':rate_mux }
            ]   
        )
        launch_description.add_action(vero_mux)
    # --------------------------------------------------

    return launch_description