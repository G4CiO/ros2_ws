#!/usr/bin/python3

from my_controller.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist, Point, Vector3 ,TransformStamped#cmd_vel, mouse_position

from nav_msgs.msg import Odometry # ไว้บอกตำแหน่ง x y ของตัวเองว่าเป็นค่าเท่าไหร่เทียบกับ frame odometry
from tf2_ros import TransformBroadcaster
from tf_transformations import euler_from_quaternion

from geometry_msgs.msg import PoseStamped

class PointToPointControllerNode(Node):
    def __init__(self):
        super().__init__('point_to_point_controller_node')

        self.declare_parameter("frequency", 100.0)
        self.frequency = self.get_parameter("frequency").get_parameter_value().double_value

        self.x_bot = 0.0
        self.y_bot = 0.0
        self.yaw_bot = 0.0
        self.state = 0
        self.goal_x = 0.0
        self.goal_y =0.0
        self.distance = 0.0
        # pid parameter
        self.linear_kp = 1.0
        self.angular_kp = 1.0

        self.target_x = 0.0
        self.target_y = 0.0
        # subscribe
        self.subscriber_goal_pose = self.create_subscription(PoseStamped, '/goal_pose', self.callback_goal_pose, 10)
        self.odom_robot_sub = self.create_subscription(Odometry, '/odom', self.callback_odom, 10)

        # publish
        self.publisher_cmd_vel = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer_cmd_vel = self.create_timer(1/self.frequency, self.publish_cmd_vel)
        
        self.get_logger().info("PointToPointController node started")


    def callback_odom(self, msg: Odometry):
        self.x_bot = msg.pose.pose.position.x
        self.y_bot = msg.pose.pose.position.y
        # Extract quaternion orientation
        quaternion = (
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w
        )
        
        # Convert quaternion to Euler angles
        _, _, self.yaw_bot = euler_from_quaternion(quaternion)  # Yaw is the heading angle

        
        
    def controller(self,x,y):
        delta_x = x - self.x_bot
        delta_y = y - self.y_bot
        self.distance = math.hypot(delta_x, delta_y)

        mouse_angle = math.atan2(delta_y, delta_x)
        error_angle = mouse_angle - self.yaw_bot
        error_radian = math.atan2(math.sin(error_angle), math.cos(error_angle))

        self.linear_vel = self.linear_kp * self.distance
        self.angular_vel = self.angular_kp * error_radian

    def callback_goal_pose(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y

    def publish_cmd_vel(self):
        self.controller(self.goal_x, self.goal_y)
        twist_msg = Twist()

        if math.fabs(self.distance) < 0.001:
            twist_msg.angular = Vector3(x = 0.0, y = 0.0, z = 0.0)
            twist_msg.linear = Vector3(x = 0.0, y = 0.0, z = 0.0)
        else:
            twist_msg.linear = Vector3(x = self.linear_vel, y = 0.0, z = 0.0)
            twist_msg.angular = Vector3(x = 0.0, y = 0.0, z = self.angular_vel)
        self.publisher_cmd_vel.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PointToPointControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
