from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    # สาทารถเขียนแบบสร้างตัวแปรก็ได้(ใช้ในกรณีที่มีชื่อ topic ซ้ำกันในแต่ละ node)
    remap_number_topic = ("number", "my_number") #(oid name, new name)

    # create name node
    number_publisher_node = Node(
        # name of directory
        package="my_py_pkg",
        # name of executable
        executable="number_publisher",
        # rename node
        name="my_number_publisher",
        # rename topic name (ใช้วิธีนี้เปลี่ยนชื่อ service ก็ได้)
        remappings=[
            remap_number_topic #(oid name, new name)
        ],
        # add parameter new value
        parameters=[
            {"number_to_publish": 4},
            {"publish_frequency": 5.0}
        ]
    )
    # create name node
    number_counter_node = Node(
        package="my_cpp_pkg",
        executable="number_counter",
        name="my_number_counter",
        remappings=[
            remap_number_topic,
            ("number_count", "my_number_count")
        ]
    )


    # add to the launch description
    ld.add_action(number_publisher_node)
    ld.add_action(number_counter_node)
    return ld