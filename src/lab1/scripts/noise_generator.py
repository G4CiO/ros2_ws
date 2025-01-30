#!/usr/bin/python3

from lab1.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node

import sys
from std_msgs.msg import Float64
from my_robot_interfaces.srv import SetNoise
import numpy as np


class NoiseGeneratorNode(Node):
    def __init__(self):
        super().__init__('noise_generator')
        # create publisher for topic /noise
        self.noise_publisher = self.create_publisher(Float64, 'noise', 10)
        # set parameter (ต้อง set ก่อน run node ไม่งั้นจะไม่มีผล)
        self.declare_parameter('rate', 5.0)
        self.rate = self.get_parameter('rate').get_parameter_value().double_value

        # # set the publisher rate (set argument) (เป็นวิธี set parameter ของ python)
        # if len(sys.argv) >= 1: # sys.argv = ['path name','data']
        #     self.rate = float(sys.argv[1])
        # else:
        #     self.rate = 5.0

        # add attribures
        self.mean = 0.0
        self.variance = 1.0
        # create service server for /set_noise
        self.set_noise_server = self.create_service(SetNoise, 'set_noise', self.set_noise_callback)
        # start a timer or publishing /noise
        self.timer = self.create_timer(1/self.rate, self.timer_callback)

        self.get_logger().info(f'Starting {self.get_namespace()} / {self.get_name()} with the default parameter. hz: {self.rate}, mean: {self.mean}, variance: {self.variance}')

    def set_noise_callback(self, request:SetNoise.Request, response:SetNoise.Response):
        self.mean = request.mean.data
        self.variance = request.variance.data
        return response

    def timer_callback(self):
        msg = Float64()
        msg.data = np.random.normal(self.mean, np.sqrt(self.variance)) # publish Random noise
        self.noise_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NoiseGeneratorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
