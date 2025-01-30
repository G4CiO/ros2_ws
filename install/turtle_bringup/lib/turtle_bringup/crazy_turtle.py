#!/usr/bin/python3

from turtle_bringup.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node

from turtlesim.srv import Spawn
import math
from geometry_msgs.msg import Twist, Point, Vector3 ,TransformStamped#cmd_vel, mouse_position
from turtlesim.msg import Pose #pose
from turtlesim_plus_interfaces.srv import GivePosition #spawn_pizza
from std_srvs.srv import Empty #eat

from nav_msgs.msg import Odometry # ไว้บอกตำแหน่ง x y ของตัวเองว่าเป็นค่าเท่าไหร่เทียบกับ frame odometry
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler

from geometry_msgs.msg import PoseStamped
from functools import partial
from turtlesim_plus_interfaces.msg import ScannerDataArray
from controller_interfaces.srv import SetParam



class CrazyTurtleNode(Node):
    def __init__(self):
        super().__init__('crazy_turtle')

        self.declare_parameter("frequency", 10.0)
        self.frequency = self.get_parameter("frequency").get_parameter_value().double_value

        self.distance = 0.0
        self.turtle2_x = 0.0
        self.turtle2_y = 0.0
        self.turtle2_angle = 0.0
        self.crazy_pizza_x = 7.5
        self.crazy_pizza_y = 5.5

        # pid parameter
        self.linear_kp = 3.0
        self.angular_kp = 8.0

        self.target_x = 0.0
        self.target_y = 0.0
        # Initialize scan_type with a default value
        # self.scan_type = 'Unknown'

        # subscribe
        self.subscriber_pose_crazy_pizza = self.create_subscription(Pose, '/crazy_pizza', self.callback_crazy_pizza, 10)
        self.subscriber_turtl2_pose = self.create_subscription(Pose, 'pose', self.callback_turtle2_pose, 10)
        # self.subscriber_scan = self.create_subscription(ScannerDataArray, 'scan', self.callback_scan, 10)

        # publish
        self.publisher_cmd_vel = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer_cmd_vel = self.create_timer(1/self.frequency, self.publish_cmd_vel)
        # server client
        self.spawn_pizza_client = self.create_client(GivePosition, '/spawn_pizza') 
        self.eat_pizza_client = self.create_client(Empty, 'eat')

        self.set_param = self.create_service(SetParam, 'gain', self.set_param_callback)

        # spawn turtle2
        # self.call_spawn_turtle2(11.0, 0.0, self.name_turtle)

    # def callback_scan(self, msg):
    #     # Ensure there is at least one element in msg.data
    #     if msg.data:
    #         self.scan_type = msg.data[0].type
    #     else:
    #         self.get_logger().warn("Received empty ScannerDataArray message.")
    #         self.scan_type = 'Unknown'

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

    def callback_crazy_pizza(self, msg):
        self.crazy_pizza_x = msg.x
        self.crazy_pizza_y = msg.y
        self.call_spawn_pizza(self.crazy_pizza_x, self.crazy_pizza_y)




    def callback_turtle2_pose(self, msg):
        self.turtle2_x = msg.x
        self.turtle2_y = msg.y
        self.turtle2_angle = msg.theta

        delta_x = self.crazy_pizza_x - self.turtle2_x
        delta_y = self.crazy_pizza_y - self.turtle2_y
        self.distance = math.hypot(delta_x, delta_y)

        mouse_angle = math.atan2(delta_y, delta_x)
        error_angle = mouse_angle - self.turtle2_angle
        error_radian = math.atan2(math.sin(error_angle), math.cos(error_angle))

        self.linear_vel = self.linear_kp * self.distance
        self.angular_vel = self.angular_kp * error_radian

    # def call_spawn_turtle2(self, x, y, name):    
    #     while not self.spawn_turtle2_client.wait_for_service(1.0):
    #         self.get_logger().warn("Waiting for Server Turtlesim Plus in 1...")    
    #     request_position = Spawn.Request()
    #     request_position.x = x
    #     request_position.y = y
    #     request_position.name = name

    #     future=self.spawn_turtle2_client.call_async(request_position)
    #     future.add_done_callback(partial(self.callback_spawn_turtle2, x=x, y=y, name=name))

    # def callback_spawn_turtle2(self, future, x, y, name):
    #     try:
    #         response = future.result()  #result function is specific to the future object
    #         self.get_logger().info(f'{name} x: {x}, y: {y}')
    #     except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
    #         self.get_logger().error("Service call failed %r" % (e, ))

    def call_spawn_pizza(self, x, y):
        while not self.spawn_pizza_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Turtlesim Plus in 2...")    
        request_position = GivePosition.Request()
        request_position.x = x
        request_position.y = y
        self.spawn_pizza_client.call_async(request_position)

    def call_eat_pizza(self):
        while not self.eat_pizza_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Turtlesim Plus in 3...")    
        repuest_eat_pizza = Empty.Request()
        self.eat_pizza_client.call_async(repuest_eat_pizza)
    
    def set_param_callback(self, request:SetParam.Request, response:SetParam.Response):
        self.linear_kp = request.kp_linear.data
        self.angular_kp = request.kp_angular.data
        return response
    

def main(args=None):
    rclpy.init(args=args)
    node = CrazyTurtleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
