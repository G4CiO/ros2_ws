#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped, Vector3
from nav_msgs.msg import Odometry
import math
import numpy as np

class PurePursuit(Node):
    def __init__(self):
        super().__init__('pure_pursuit')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.timer = self.create_timer(0.1, self.pure_pursuit_control)
        
        x_values = np.linspace(0, 5, num=50)
        self.waypoints = [(x, math.sin(2 * math.pi * x / 5)) for x in x_values]
        
        self.current_index = 0
        self.lookahead_distance = 1.0  # ระยะมองไปข้างหน้า
        self.position = (0.0, 0.0)
        self.yaw = 0.0
        self.linear_velocity = 1.0  # Fixed linear velocity
        # self.max_angular_speed = 1.0  # Maximum angular velocity
        # pid parameter
        # self.linear_kp = 0.1
        # self.angular_kp = 0.1

    def odom_callback(self, msg:Odometry):
        self.position = (msg.pose.pose.position.x, msg.pose.pose.position.y)
        orientation_q = msg.pose.pose.orientation
        siny_cosp = 2 * (orientation_q.w * orientation_q.z + orientation_q.x * orientation_q.y)
        cosy_cosp = 1 - 2 * (orientation_q.y * orientation_q.y + orientation_q.z * orientation_q.z)
        self.yaw = math.atan2(siny_cosp, cosy_cosp)

    def pure_pursuit_control(self):
        if self.current_index >= len(self.waypoints):
            self.current_index = 0  # Reset index to loop the path
        # Implement Here

        goal_x, goal_y = self.waypoints[self.current_index]
        dx = goal_x - self.position[0]
        dy = goal_y - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        print(f'distance: {distance} < lookahead_distance: {self.lookahead_distance}',f'index: {self.current_index}')

        # If distance < lookahead_distance, it moves to the next waypoint.
        if distance < self.lookahead_distance:
            self.current_index += 1

        # Heading Angle Calculation
        target_angle = math.atan2(dy, dx)
        alpha = target_angle - self.yaw
        
        # Steering Angle Calculation (β)
        # beta = math.atan2(2 * 0.2 * math.sin(alpha), self.lookahead_distance)
        # 0.2 is wheelbase (distance between front and rear wheels) in an Ackermann vehicle.
        
        # Angular Velocity Calculation (ω)
        angular_velocity = 2 * self.linear_velocity * math.sin(alpha) / self.lookahead_distance

        # Publish cmd_vel
        msg = Twist()
        msg.linear.x = self.linear_velocity
        msg.angular.z = angular_velocity
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PurePursuit()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
