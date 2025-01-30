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

class OdomPublisherNode(Node):
    def __init__(self):
        super().__init__('odom_publisher')
        # name odom parameter
        self.declare_parameter("nameturtle1", 'A')
        self.nameturtle1 = self.get_parameter("nameturtle1").value
        self.declare_parameter("nameturtle2", 'B')
        self.nameturtle2 = self.get_parameter("nameturtle2").value
        # subscribtion
        self.subscriber_turtle1_pose = self.create_subscription(Pose, f'/{self.nameturtle1}/pose', self.callback_turtle1_pose, 10)
        self.subscriber_turtle2_pose = self.create_subscription(Pose, f'/{self.nameturtle2}/pose', self.callback_turtle2_pose, 10)
        # odom/TF
        self.odom1_publisher = self.create_publisher(Odometry, '/odom1', 10)
        self.odom2_publisher = self.create_publisher(Odometry, '/odom2', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        
    def callback_turtle1_pose(self, msg):
        self.turtle1_x = msg.x
        self.turtle1_y = msg.y
        self.turtle1_angle = msg.theta

        self.pub(self.turtle1_x,self.turtle1_y,self.turtle1_angle,self.nameturtle1,'odom')
        
    def callback_turtle2_pose(self, msg):
        self.turtle2_x = msg.x
        self.turtle2_y = msg.y
        self.turtle2_angle = msg.theta

        self.pub(self.turtle2_x,self.turtle2_y,self.turtle2_angle,self.nameturtle2,'odom')

    def pub(self, x,y,angle, child_frame_id,head_frame_id):

        # create odom and send
        odom_msg = Odometry()
        odom_msg.header.frame_id = head_frame_id
        odom_msg.header.stamp = self.get_clock().now().to_msg() # stamp = เวลาของ msg
        odom_msg.child_frame_id = child_frame_id
        # Position
        odom_msg.pose.pose.position.x = x - 5.5
        odom_msg.pose.pose.position.y = y - 5.5
        # Orentation
        q = quaternion_from_euler(0, 0, angle)
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]
        # self.odom_publisher.publish(odom_msg)

        # Publish the odom message
        if child_frame_id == self.nameturtle1:
            self.odom1_publisher.publish(odom_msg)
        elif child_frame_id == self.nameturtle2:
            self.odom2_publisher.publish(odom_msg)

        # create TF and send
        t = TransformStamped()
        t.header.frame_id = head_frame_id
        t.header.stamp = self.get_clock().now().to_msg()
        t.child_frame_id = child_frame_id
        # Translation
        t.transform.translation.x = x - 5.5
        t.transform.translation.y = y - 5.5
        # Rotation
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        # Broadcast TF
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomPublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()

# from turtle_bringup.dummy_module import dummy_function, dummy_var
# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import Twist, Point, TransformStamped, PoseStamped
# from turtlesim.msg import Pose
# import numpy as np

# from turtlesim_plus_interfaces.srv import GivePosition
# from std_srvs.srv import Empty
# from nav_msgs.msg import Odometry
# from tf2_ros import TransformBroadcaster
# from tf_transformations import quaternion_from_euler

# from std_msgs.msg import Int64

# class OdomPublisherNode(Node):
#     def __init__(self):
#         super().__init__('odom_publisher_node')
        
#         self.odom1_pub_ = self.create_publisher(Odometry, 'odom1', 10)
#         self.odom2_pub_ = self.create_publisher(Odometry, 'odom2', 10)
        
#         self.tf_broadcaster_ = TransformBroadcaster(self)
        
#         self.declare_parameter('nameturtle1','turtleX')
#         self.turtle_name1 = self.get_parameter('nameturtle1').value

#         self.declare_parameter('nameturtle2','turtleX')
#         self.turtle_name2 = self.get_parameter('nameturtle2').value

#         self.create_subscription(Pose,f'{self.turtle_name1}/pose',self.t1_pose_callback,10)

#         self.create_subscription(Pose,f'{self.turtle_name2}/pose',self.t2_pose_callback,10)
        
#         self.tt1_pose = np.array([0.0, 0.0, 0.0]) # x, y, theta
#         self.tt2_pose = np.array([0.0, 0.0, 0.0]) # x, y, theta
        
        
#         self.control_loop_timer_ = self.create_timer(0.01, self.timer_callback)
        
#     def t1_pose_callback(self,msg1):
#         self.tt1_pose[0] = msg1.x 
#         self.tt1_pose[1] = msg1.y 
#         self.tt1_pose[2] = msg1.theta
#         self.odom_pub(self.odom1_pub_,self.tt1_pose,self.turtle_name1)
#         # print(self.tt1_pose)
    
#     def t2_pose_callback(self,msg2):
#         self.tt2_pose[0] = msg2.x 
#         self.tt2_pose[1] = msg2.y 
#         self.tt2_pose[2] = msg2.theta 
#         self.odom_pub(self.odom2_pub_,self.tt2_pose,self.turtle_name2)
#         # print(self.tt2_pose)
    
    
#     def odom_pub(self,odom_pub,pose,child_frame_id):
#         odom = Odometry()
#         odom.header.stamp = self.get_clock().now().to_msg()
#         odom.header.frame_id = 'odom'
#         odom.child_frame_id = child_frame_id
        
#         odom.pose.pose.position.x = pose[0]
#         odom.pose.pose.position.y = pose[1]
        
#         q = quaternion_from_euler(0, 0, pose[2]) # Orientation data of ROS2 is Quaternion so convert euler to quaternion
#         odom.pose.pose.orientation.x = q[0]
#         odom.pose.pose.orientation.y = q[1]
#         odom.pose.pose.orientation.z = q[2]
#         odom.pose.pose.orientation.w = q[3]
        
#         odom_pub.publish(odom)
        
#         t = TransformStamped()
#         t.header.stamp = self.get_clock().now().to_msg()
#         t.header.frame_id = 'odom'
#         t.child_frame_id = child_frame_id
        
#         t.transform.translation.x = pose[0]
#         t.transform.translation.y = pose[1]
#         t.transform.rotation.x = q[0]
#         t.transform.rotation.y = q[1]
#         t.transform.rotation.z = q[2]
#         t.transform.rotation.w = q[3]
        
#         self.tf_broadcaster_.sendTransform(t)
        
#     def timer_callback(self):
#         # print(self.tt1_pose,self.tt2_pose)
#         pass
        

# def main(args=None):
#     rclpy.init(args=args)
#     node = OdomPublisherNode()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__=='__main__':
#     main()