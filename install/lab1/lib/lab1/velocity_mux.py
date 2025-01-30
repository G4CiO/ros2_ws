#!/usr/bin/python3

from lab1.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import sys


class VelocityMuxNode(Node):
    def __init__(self):
        super().__init__('velocity_mux')
        # set parameter (ต้อง set ก่อน run node ไม่งั้นจะไม่มีผล)
        self.declare_parameter('rate', 5.0)
        self.rate = self.get_parameter('rate').get_parameter_value().double_value

        # create subscriber or topic /linear/noise
        self.linear_vel_subcriber = self.create_subscription(Float64, '/linear/noise', self.linear_vel_sub_callback, 10)
        # create subscriber or topic /angular/noise
        self.angular_vel_subcriber = self.create_subscription(Float64, '/angular/noise', self.angular_sub_callback, 10)
        # create publisher for topic /cmd_vel
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # add attrobutes
        self.cmd_vel = Twist() # create msg Twist
        # start timer for publishing /cmd_vel
        self.timer = self.create_timer(1/self.rate, self.timer_callback)

        self.get_logger().info(f'Starting {self.get_name()}')

    # publish cmd_vel
    def timer_callback(self):
        self.cmd_vel_publisher.publish(self.cmd_vel)

    # Callback : sent the x component of linear velocity
    def linear_vel_sub_callback(self, msg:Float64):
        self.cmd_vel.linear.x = msg.data
    # Callback : sent the z component of angular velocity
    def angular_sub_callback(self, msg:Float64):
        self.cmd_vel.angular.z = msg.data


def main(args=None):
    rclpy.init(args=args)
    node = VelocityMuxNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
