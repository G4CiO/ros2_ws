#!/usr/bin/python3

import roboticstoolbox as rtb
import numpy as np
from spatialmath import SE3
from math import pi
from math import radians

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import TransformStamped, PoseStamped
from tf2_msgs.msg import TFMessage
import tf_transformations

class EndEffectorPose_(Node):

    def __init__(self):
        super().__init__('end_effector_pose_')

        # Create a buffer and listener for transforms
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Create a publisher for the PoseStamped message
        self.pose_pub = self.create_publisher(PoseStamped, '/end_effector', 10)
        # Create a Subscriber tf
        self.tf_sub = self.create_subscription(TFMessage, '/tf', self.callback_tf, 10)

        # Set the source and target frames (replace with your frames)
        self.source_frame = 'link_0'
        self.target_frame = 'end_effector'

        # Timer to periodically check for transform
        # self.timer = self.create_timer(1.0, self.get_transform)

    # def callback_tf(self, msg:TFMessage):
    #     tf_data = msg.transforms[0]
    #     h1 = tf_data.
    #     self.get_logger().info(self.tf_data)

    def callback_tf(self, msg: TFMessage):
        joint1 = msg.transforms[0]
        joint2 = msg.transforms[1]
        joint3 = msg.transforms[2]

        T01 = self.transformation(joint1)
        T12 = self.transformation(joint2)
        T2e = self.transformation(joint3)

        T0e = T01 @ T12 @ T2e

        self.get_logger().info(f'T0e:{T0e}')

        # self.get_logger().info('T0e:')
        # self.get_logger().info(f'{T0e}')

        for transform in msg.transforms:
            self.process_transform(transform)
            self.print_transform(transform)

    def process_transform(self, transform):
        # Extract translation (x, y, z)
        x = transform.transform.translation.x
        y = transform.transform.translation.y
        z = transform.transform.translation.z

        # Extract rotation (quaternion)
        qx = transform.transform.rotation.x
        qy = transform.transform.rotation.y
        qz = transform.transform.rotation.z
        qw = transform.transform.rotation.w

        # Create a PoseStamped message
        pose_msg = PoseStamped()

        # Fill in the PoseStamped header
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = transform.header.frame_id

        # Set the position (translation)
        pose_msg.pose.position.x = x
        pose_msg.pose.position.y = y
        pose_msg.pose.position.z = z

        pose_msg.pose.orientation.x = qx
        pose_msg.pose.orientation.y = qy
        pose_msg.pose.orientation.z = qz
        pose_msg.pose.orientation.w = qw

        # Publish the PoseStamped message
        self.pose_pub.publish(pose_msg)

    def transformation(self, joint):
        # Extract translation (x, y, z)
        x = joint.transform.translation.x
        y = joint.transform.translation.y
        z = joint.transform.translation.z

        # Extract rotation (quaternion)
        qx = joint.transform.rotation.x
        qy = joint.transform.rotation.y
        qz = joint.transform.rotation.z
        qw = joint.transform.rotation.w

        # Convert quaternion to roll, pitch, yaw
        RPY = tf_transformations.euler_from_quaternion([qx, qy, qz, qw])

        # Desired end effector pose
        T_Position = SE3(x, y, z)
        # Desired end effector oren
        T_Orentation = SE3.RPY([RPY[0], RPY[1], RPY[2]], order='zyx')
        # TF of End-Effector
        TF = T_Position @ T_Orentation

        return TF

    def print_transform(self, transform):
        # Log information about each TransformStamped in the message
        self.get_logger().info(f"Received transform from {transform.header.frame_id} to {transform.child_frame_id}:")
        self.get_logger().info(f"Translation: {transform.transform.translation}")
        self.get_logger().info(f"Rotation: {transform.transform.rotation}")

    

def main(args=None):
    rclpy.init(args=args)
    node = EndEffectorPose_()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()




