#!/bin/python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class SmartphoneNode(Node): 
    def __init__(self):
        super().__init__("smartphone") 

        self.subscriber_ = self.create_subscription(String, "robot_news", self.callback_robot_news, 10) #(msg_type, topic name (should same name as publish topic), call back msg from publish, size)
        
        self.get_logger().info("Smartphone has been stared")
    
    #sucscribe data from robot news station publish
    def callback_robot_news(self, msg):
        self.get_logger().info(msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = SmartphoneNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()