#!/bin/python3
import rclpy
from rclpy.node import Node

from my_robot_interfaces.srv import ComputeRectangleArea

class ComputeRectangleAreaServerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("compute_rectangle_area_server") # MODIFY NAME

        # create service server
        self.server_ = self.create_service(
            ComputeRectangleArea, "compute_rectangle_area", self.call_back_compute_rectangle_area)    #(service type, service name, callback function)
                                                                        #service name should begin with Verb and follow by Object that you do

        self.get_logger().info("Compute rectangle area server has been stared.")

    #when send request this callback function will process request and return response.
    def call_back_compute_rectangle_area(self, request, response):
        #computation for return response
        response.area = 0.5 * request.length * request.width

        # print result computation on terminal
        self.get_logger().info("1/2 * " + str(request.length) + " * " + str(request.width) + " = " + str(response.area))

        return response #don't forget return responce. it will error

def main(args=None):
    rclpy.init(args=args)
    node = ComputeRectangleAreaServerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()