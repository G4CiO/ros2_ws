#!/usr/bin/python3

from my_controller.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Pose, PoseWithCovariance, Quaternion, Twist, TwistWithCovariance, Vector3, TransformStamped, Pose2D
from std_msgs.msg import Float64MultiArray
from nav_msgs.msg import Odometry
from std_msgs.msg import Header, Float32
from tf2_ros import TransformBroadcaster
import tf_transformations
from math import cos,sin,pi


class DiffDriveNode(Node):
    def __init__(self):
        super().__init__('diff_drive_node')
        # Robot parameters
        self.declare_parameter("frequency", 100.0)
        self.frequency = self.get_parameter("frequency").get_parameter_value().double_value
        self.wheel_base = 0.35 # Distance between the wheels (meters)
        self.wheel_radius = 0.05  # Radius of the wheels (meters)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.last_callback_time = self.get_clock().now()
        self.initial_orientation = None
        self.yaw_dot = 0.0
        self.ax = 0.0
        
        
        # Subscribers
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        # Initialize the transform broadcaster
        self.tf_br = TransformBroadcaster(self)
        self.isOdomUpdate = False

        # Initialize odometry variables
        self.odom_msg = Odometry(
            header=Header(
                stamp=self.get_clock().now().to_msg(),
                frame_id='odom'
            ),
            child_frame_id='base_link',
            pose=PoseWithCovariance(
                pose=Pose(
                    position=Point(
                        x=0.0,
                        y=0.0,
                        z=0.0
                    ),
                    orientation=Quaternion(
                        x=0.0,
                        y=0.0,
                        z=0.0,
                        w=1.0
                    )
                )
            ),
            twist=TwistWithCovariance(
                twist=Twist(
                    linear=Vector3(
                        x=0.0,
                        y=0.0,
                        z=0.0
                    ),
                    angular=Vector3(
                        z=0.0
                    )
                )
            )
        )


        
        # Publishers
        self.wheel_velo_pub = self.create_publisher(Float64MultiArray, '/velocity_controllers/commands', 10)
        self.pose_pub = self.create_publisher(Pose2D, '/pose', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.timer_pose = self.create_timer(1/self.frequency, self.timer_callback)

        self.get_logger().info("DiffDriveController node started")

    def cmd_vel_callback(self, msg: Twist):
        # Extract linear and angular velocities
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

        
        # self.get_logger().info(f"Published wheel velocities: left={v_left:.2f}, right={v_right:.2f}")

    def wheel_velo_callback(self):
        factor = 1 / self.wheel_radius
        # Calculate wheel velocities            
        # [ϕ̇_L]   [ 1/r  -B/(2r) ] [v_robot]
        # [ϕ̇_R] = [ 1/r   B/(2r) ] [ω_robot]
        v_left = factor * (self.linear_velocity - (self.wheel_base / 2) * self.angular_velocity)
        v_right = factor * (self.linear_velocity + (self.wheel_base / 2) * self.angular_velocity)

        # Publish wheel velocities
        command_msg = Float64MultiArray()
        command_msg.data = [v_left, v_right]
        self.wheel_velo_pub.publish(command_msg)

    def pose_callback(self, linear_velocity, angular_velocity, dt):
         dx = linear_velocity * cos(self.theta)*dt
         dy = linear_velocity * sin(self.theta)*dt
         dtheta = angular_velocity * dt

         self.x+=dx
         self.y+=dy
         self.theta+=dtheta

         msg = Pose2D()
         msg.x = self.x
         msg.y = self.y
         msg.theta = self.theta

         self.pose_pub.publish(msg)

    def odom_callback(self):
        quaternion = tf_transformations.quaternion_from_euler(0.0, 0.0, self.theta)
        # Create Odometry message and fill in the data
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()  # Update time stamp
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'
        odom_msg.pose.pose = Pose(
            position=Point(x=self.x, y=self.y, z=0.0),
            orientation=Quaternion(
            x=quaternion[0],
            y=quaternion[1],
            z=quaternion[2],
            w=quaternion[3]
        )
        )
        odom_msg.twist.twist.linear = Vector3(x=self.linear_velocity , y=0.0, z=0.0)
        odom_msg.twist.twist.angular = Vector3(x=0.0, y=0.0, z=self.angular_velocity)

        
        
        transform = TransformStamped()
        transform.header.stamp = odom_msg.header.stamp
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_link'  # Make sure it matches the child frame ID in odom_output
        transform.transform.translation.x = odom_msg.pose.pose.position.x
        transform.transform.translation.y = odom_msg.pose.pose.position.y
        transform.transform.translation.z = odom_msg.pose.pose.position.z
        transform.transform.rotation = odom_msg.pose.pose.orientation
        
        self.odom_pub.publish(odom_msg)
        self.tf_br.sendTransform(transform)

    def timer_callback(self):
        # Calculate pose robot
        self.wheel_velo_callback()
        self.pose_callback(self.linear_velocity, self.angular_velocity, 1/self.frequency)
        self.odom_callback()

def main(args=None):
    rclpy.init(args=args)
    node = DiffDriveNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
