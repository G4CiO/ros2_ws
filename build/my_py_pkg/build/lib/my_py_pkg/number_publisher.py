#!/bin/python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__("number_publisher")

        # Parameter
        # ----------------------------------------------------------------------------------------------------------------------
        # declare new parameter and set parameter
        self.declare_parameter("number_to_publish", 2) # (name_param, default value) name of set and get parameter must be same
        self.declare_parameter("publish_frequency", 1.0)

        # get parameter from the node
        # it will return parameter object
        self.number = self.get_parameter("number_to_publish").value # (name_param) ".value" for get actual value)
        self.publisher_frequency = self.get_parameter("publish_frequency").value
        # ----------------------------------------------------------------------------------------------------------------------

        self.publishers_ = self.create_publisher(Int64, "number", 10)

        self.timer_ = self.create_timer(1.0 / self.publisher_frequency, self.publish_number)

        self.get_logger().info("Number Publisher has been stared")

    def publish_number(self):
        msg = Int64()
        msg.data = self.number  
        self.publishers_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()