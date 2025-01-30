#!/usr/bin/python3

from lecture2.dummy_module import dummy_function, dummy_var
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

class TurtlesimPlusController(Node):
    def __init__(self):
        super().__init__('turtlesimplus_controller')

        self.get_logger().info('turtlesimplus controller node has been start.')

        self.distance = 0.0
        self.turtle2_x = 0.0
        self.turtle2_y = 0.0
        self.turtle2_angle = 0.0
        # Initialize mouse position attributes with default values
        self.mouse_x = 5.5
        self.mouse_y = 5.5

        # pid parameter
        self.declare_parameter("linear_kp", 3)
        self.linear_kp = self.get_parameter("linear_kp").value

        self.declare_parameter("angular_kp", 8)
        self.angular_kp = self.get_parameter("angular_kp").value

        # subscribe
        self.subscriber_turtle_pose = self.create_subscription(Pose, '/turtle1/pose', self.callback_turtle1_pose, 10)
        self.subscriber_turtle_pose = self.create_subscription(Pose, '/turtle2/pose', self.callback_turtle2_pose, 10)
        self.subscriber_mouse_pose = self.create_subscription(Point, '/mouse_position', self.callback_mouse_position, 10)

        # publish
        self.publisher_cmd_vel = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer_cmd_vel = self.create_timer(0.01, self.publish_cmd_vel)
        # odom/TF
        self.odom_publisher = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # server client
        self.spawn_pizza_client = self.create_client(GivePosition, 'spawn_pizza')
        self.eat_pizza_client = self.create_client(Empty, '/turtle1/eat')
        self.timer_eat_pizza = self.create_timer(0.01, self.call_eat_pizza)

    def publish_cmd_vel(self):
        twist_msg = Twist()
        # if math.fabs(self.distance) < 5.0:
        #     self.call_eat_pizza()
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

        x = '%.5f' %(self.mouse_x)
        y = '%.5f' %(self.mouse_y)
        self.get_logger().info(f'Go to the target x: {x}, y: {y}.')

    def callback_turtle1_pose(self, msg):
        turtle1_x = msg.x
        turtle1_y = msg.y
        turtle1_angle = msg.theta

        # delta_x = self.turtle2_x - turtle1_x
        # delta_y = self.turtle2_y - turtle1_y
        # self.distance = math.hypot(delta_x, delta_y)

        # self.turtle2_angle = math.atan2(delta_y, delta_x)
        # error_angle = self.turtle2_angle - turtle1_angle
        # error_radian = math.atan2(math.sin(error_angle), math.cos(error_angle))

        # self.linear_vel = self.linear_kp * self.distance
        # self.angular_vel = self.angular_kp * error_radian

        delta_x = self.mouse_x - turtle1_x
        delta_y = self.mouse_y - turtle1_y
        self.distance = math.hypot(delta_x, delta_y)

        mouse_angle = math.atan2(delta_y, delta_x)
        error_angle = mouse_angle - turtle1_angle
        error_radian = math.atan2(math.sin(error_angle), math.cos(error_angle))

        self.linear_vel = self.linear_kp * self.distance
        self.angular_vel = self.angular_kp * error_radian

        #//////////////////////////////////////////////////////
        # create odom and send
        odom_msg = Odometry()
        odom_msg.header.frame_id = "odom"
        odom_msg.header.stamp = self.get_clock().now().to_msg() # stamp = เวลาของ msg
        odom_msg.child_frame_id = "robot"
        # Position
        odom_msg.pose.pose.position.x = turtle1_x
        odom_msg.pose.pose.position.y = turtle1_y
        # Orentation
        q = quaternion_from_euler(0, 0, turtle1_angle)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]
        # Velocity (ไม่ใส่เพราะ turtle1_pose ไม่มีการ publish ออกมา)
        # odom_msg.twist.twist.linear.x = 
        # odom_msg.twist.twist.linear.y = 
        # odom_msg.twist.twist.angular.z = 
        self.odom_publisher.publish(odom_msg)

        # create TF and send
        t = TransformStamped()
        t.header.frame_id = "odom"
        t.header.stamp = self.get_clock().now().to_msg()
        t.child_frame_id = "robot"
        # Translation
        t.transform.translation.x = turtle1_x
        t.transform.translation.y = turtle1_y
        # Rotation
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        # Broadcast TF
        self.tf_broadcaster.sendTransform(t)

    def callback_turtle2_pose(self, msg):
        self.turtle2_x = msg.x
        self.turtle2_y = msg.y
        self.turtle2_angle = msg.theta


    def call_spawn_pizza(self, x, y):        
        request_position = GivePosition.Request()
        request_position.x = x
        request_position.y = y

        self.spawn_pizza_client.call_async(request_position)

    def call_eat_pizza(self):
        repuest_eat_pizza = Empty.Request()
        self.eat_pizza_client.call_async(repuest_eat_pizza)

    # def timer_callback(self):




    

def main(args=None):
    rclpy.init(args=args)
    node = TurtlesimPlusController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
