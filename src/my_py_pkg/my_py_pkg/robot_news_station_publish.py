#!/bin/python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import String #When you depend on another package, you will need to add a dependency in "package.xml" file

class RobotNewStationNode(Node): 
    def __init__(self):
        super().__init__("robot_news_station") #should use the same name for the "file" and "node name" and "executable name"
        
        # set parameter
        self.declare_parameter("robot_name", "ATOM")
        # get parameter from the node
        self.robot_name_ = self.get_parameter("robot_name").value
        
        # create publisher
        self.publishers_ = self.create_publisher(String, "robot_news", 10) #(msg_type, topic name, queue size of topic)
        #create timer to publish data
        self.timer_ = self.create_timer(0.5, self.publish_news) #It will publish topic that have data "Hello" every 0.5 second

        self.get_logger().info("Robot News Station has been stared")

    #This function will published data on the topic robot_news
    def publish_news(self):
        #create empty string object 
        msg = String()
        #set message data
        msg.data = "Hi. my name is " +str(self.robot_name_) + " from Real Steel."  
        #publish message on the topic robot_news
        self.publishers_.publish(msg) 

def main(args=None):
    rclpy.init(args=args)
    node = RobotNewStationNode() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()