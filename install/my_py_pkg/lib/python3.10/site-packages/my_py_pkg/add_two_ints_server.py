#!/bin/python3
import rclpy
from rclpy.node import Node

from example_interfaces.srv import AddTwoInts

class AddTwoIntsServerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("add_two_ints_server") # MODIFY NAME

        # create service server
        self.server_ = self.create_service(
            AddTwoInts, "add_two_ints", self.call_back_add_two_ints)    #(service type, service name, callback function)
                                                                        #service name should begin with Verb and follow by Object that you do

        self.get_logger().info("Add two ints server has been stared.")

    #when send request this callback function will process request and return response.
    def call_back_add_two_ints(self, request, response):
        #computation for return response
        response.sum = request.a + request.b #from ros2 interface show example_interfaces/srv/AddTwoInts

        # print result computation on terminal
        self.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(response.sum))

        return response #don't forget return responce. it will error

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()