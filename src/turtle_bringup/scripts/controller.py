#!/usr/bin/python3

from turtle_bringup.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node

import math
from geometry_msgs.msg import Twist, Point, Vector3 ,TransformStamped#cmd_vel, mouse_position
from turtlesim.msg import Pose #pose
from turtlesim_plus_interfaces.srv import GivePosition #spawn_pizza
from std_srvs.srv import Empty #eat

from nav_msgs.msg import Odometry # ไว้บอกตำแหน่ง x y ของตัวเองว่าเป็นค่าเท่าไหร่เทียบกับ frame odometry
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler

from geometry_msgs.msg import PoseStamped
from turtlesim_plus_interfaces.msg import ScannerDataArray
from controller_interfaces.srv import SetTarget
from controller_interfaces.srv import SetParam

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller')

        self.declare_parameter("frequency", 10.0)
        self.frequency = self.get_parameter("frequency").get_parameter_value().double_value

        self.state = 0
        self.goal_x = 0.0
        self.goal_y =0.0
        self.distance = 0.0
        # Initialize mouse position attributes with default values
        self.mouse_x = 11.0
        self.mouse_y = 11.0
        # pid parameter
        self.linear_kp = 3.0
        self.angular_kp = 8.0

        self.target_x = 0.0
        self.target_y = 0.0
        # Initialize scan_type with a default value
        # self.scan_type = 'Unknown'
        # subscribe
        self.subscriber_turtle_pose = self.create_subscription(Pose, 'pose', self.callback_turtle1_pose, 10)
        self.subscriber_mouse_pose = self.create_subscription(Point, '/mouse_position', self.callback_mouse_position, 10)
        self.subscriber_goal_pose = self.create_subscription(PoseStamped, '/goal_pose', self.callback_goal_pose, 10)
        # self.subscriber_scan = self.create_subscription(ScannerDataArray, 'scan', self.callback_scan, 10)

        # publish
        self.publisher_cmd_vel = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer_cmd_vel = self.create_timer(1/self.frequency, self.publish_cmd_vel)
        # server client
        self.spawn_pizza_client = self.create_client(GivePosition, '/spawn_pizza')
        self.eat_pizza_client = self.create_client(Empty, 'eat')
        # self.set_target = self.create_client(SetTarget, '/cli')
        # create service server for /set_noise
        self.set_target = self.create_service(SetTarget, 'cli', self.set_target_callback)
        self.set_param = self.create_service(SetParam, 'gain', self.set_param_callback)


        


    # def callback_scan(self, msg):
    #     # Ensure there is at least one element in msg.data
    #     if msg.data:
    #         self.scan_type = msg.data[0].type
    #     else:
    #         self.get_logger().warn("Received empty ScannerDataArray message.")
    #         self.scan_type = 'Unknown'

    def controller(self,x,y):
        delta_x = x - self.turtle1_x
        delta_y = y - self.turtle1_y
        self.distance = math.hypot(delta_x, delta_y)

        mouse_angle = math.atan2(delta_y, delta_x)
        error_angle = mouse_angle - self.turtle1_angle
        error_radian = math.atan2(math.sin(error_angle), math.cos(error_angle))

        self.linear_vel = self.linear_kp * self.distance
        self.angular_vel = self.angular_kp * error_radian

    
    def callback_goal_pose(self, msg):
        self.goal_x = msg.pose.position.x + 5.5
        self.goal_y = msg.pose.position.y +5.5

        self.call_spawn_pizza(self.goal_x, self.goal_y)
        self.state = 2
        print(self.state)
        # self.get_logger().info(self.temp)

        x = '%.5f' %(self.goal_x)
        y = '%.5f' %(self.goal_y)
        # self.get_logger().info(f'Goal target x: {x}, y: {y}.')



    def publish_cmd_vel(self):
        twist_msg = Twist()
        # if self.scan_type != 'Turtle':
        #     self.call_eat_pizza()
        if math.fabs(self.distance) < 0.8:
            self.call_eat_pizza()
        if math.fabs(self.distance) < 0.00001:
            twist_msg.angular = Vector3(x = 0.0, y = 0.0, z = 0.0)
            twist_msg.linear = Vector3(x = 0.0, y = 0.0, z = 0.0)
        else:
            twist_msg.linear = Vector3(x = self.linear_vel, y = 0.0, z = 0.0)
            twist_msg.angular = Vector3(x = 0.0, y = 0.0, z = self.angular_vel)
        self.publisher_cmd_vel.publish(twist_msg)

    def callback_mouse_position(self, msg):
        self.mouse_x = msg.x 
        self.mouse_y = msg.y
        self.call_spawn_pizza(self.mouse_x, self.mouse_y)
        self.state = 1

        x = '%.5f' %(self.mouse_x)
        y = '%.5f' %(self.mouse_y)
        # self.get_logger().info(f'Go to the target x: {x}, y: {y}.')

    def callback_turtle1_pose(self, msg):
        self.turtle1_x = msg.x
        self.turtle1_y = msg.y
        self.turtle1_angle = msg.theta
        if self.state == 1:
            self.controller(self.mouse_x, self.mouse_y)
        elif self.state == 2:
            self.controller(self.goal_x, self.goal_y)
        elif self.state == 3:
            self.controller(self.target_x, self.target_y)

    def call_spawn_pizza(self, x, y):
        while not self.spawn_pizza_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Turtlesim Plus in 4...")   
        request_position = GivePosition.Request()
        request_position.x = x
        request_position.y = y
        self.spawn_pizza_client.call_async(request_position)

    def call_eat_pizza(self):
        while not self.eat_pizza_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Turtlesim Plus in 5...")  
        repuest_eat_pizza = Empty.Request()
        self.eat_pizza_client.call_async(repuest_eat_pizza)

    def call_set_target(self, target):
        while not self.set_target.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Turtlesim Plus in 5...")  
        request_set_target = SetTarget.Request()
        request_set_target.target = target
        self.set_target.call_async(request_set_target)

    def set_target_callback(self, request:SetTarget.Request, response:SetTarget.Response):
        self.state = 3
        self.target_x = request.target.x
        self.target_y = request.target.y
        return response
    
    def set_param_callback(self, request:SetParam.Request, response:SetParam.Response):
        self.linear_kp = request.kp_linear.data
        self.angular_kp = request.kp_angular.data
        return response



def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
