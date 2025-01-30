#!/bin/python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounter(Node):
    def __init__(self):
        super().__init__("number_counter")

        self.counter_= 0

        self.subscriber_ = self.create_subscription(Int64, "number", self.callbackNumber, 10)
        
        self.publishers_ = self.create_publisher(Int64, "number_count", 10)

        # create service server
        self.server_ = self.create_service(
            SetBool, "reset_counter", self.call_back_set_bool)

        self.get_logger().info("number counter has been stared")
    
    #sucscribe data from number publisher
    def callbackNumber(self, msg):
        self.counter_ += msg.data

        #for publisher
        new_msg = Int64()
        new_msg.data = self.counter_
        self.publishers_.publish(new_msg)

    #when send request this callback function will process request and return response.
    def call_back_set_bool(self, request, response):
        #set counter_ = 0
        if request.data:
            self.counter_ = 0
            self.get_logger().info("Set Counter to 0")
            response.success = True
            response.message = "Set Counter to 0 complete"
        else:
            self.get_logger().info("Nothing change in Counter")
            response.success = False
            response.message = "Set Counter to 0 not complete"

        

        return response #don't forget return responce. it will error

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()