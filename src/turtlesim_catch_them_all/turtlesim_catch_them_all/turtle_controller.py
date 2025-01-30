#!/bin/python3
import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist, Vector3
from my_robot_interfaces.msg import Turtle #/name (name alive turtle), /coordinates
from my_robot_interfaces.srv import CatchTurtle
from functools import partial

class TurtleControllerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("turtle_controller") # MODIFY NAME
        
        # Initialize attributes
        self.alive_turtles = []
        self.alive_coordinates = []
        self.current_x = 0.0
        self.current_y = 0.0
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        # Screen boundaries
        self.screen_min_x = 0.0
        self.screen_max_x = 11.0
        self.screen_min_y = 0.0
        self.screen_max_y = 11.0

        # subscribe
        self.subscribe_avive = self.create_subscription(Turtle, "alive_turtles", self.callback_turtle_spawner, 10)
        self.subscribe_turtle1 = self.create_subscription(Pose, "turtle1/pose", self.callback_turtle1_pose, 10)

        # Initialize target coordinates
        self.target_x = 0.0
        self.target_y = 0.0
        self.Kp_linear = 2.0  # Proportional gain for linear velocity
        self.Kp_angular = 4.0  # Proportional gain for angular velocity

        # publish
        self.publisher_cmd = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.timer_cmd = self.create_timer(0.01, self.publish_cmd)

        self.get_logger().info("Turtle Controller Node has been stared")


    def publish_cmd(self):
        # Publish Twist message to control TurtleSim
        twist_msg = Twist()
        twist_msg.linear = Vector3(x=self.linear_vel, y=0.0, z=0.0)
        twist_msg.angular = Vector3(x=0.0, y=0.0, z=self.angular_vel)
        self.publisher_cmd.publish(twist_msg)

# -------------------------------------------------------------------

    # def find_closest_turtle1(other_turtle, turtle1):
    #     return other_turtle[min(range(len(other_turtle)), key = lambda i: abs(other_turtle[i]-turtle1))]

# -------------------------------------------------------------------

    def compute_vectors_for_consecutive_pairs(self, arr):  # arr = self.alive_coordinates
        vectors = []
        for i in range(len(arr) // 2):
            index = i * 2
            tx = arr[index]
            ty = arr[index + 1]
            vector = math.sqrt(((tx - self.current_x) ** 2) + ((ty - self.current_y) ** 2))
            
            vectors.append(vector)
        return vectors

# -------------------------------------------------------------------

    # def compute_vector(self, tx, ty , cx, cy):
    #     nearlest = math.sqrt(((tx-cx) ** 2) + ((ty-cy) ** 2))
    #     return nearlest

# -------------------------------------------------------------------

    def callback_turtle1_pose(self, msg):
        
        self.current_x = msg.x
        self.current_y = msg.y
        current_angle = msg.theta

        distance = math.sqrt((self.target_x - self.current_x)**2 + (self.target_y - self.current_y)**2)

        # Calculate angle to target
        desired_angle = math.atan2(self.target_y - self.current_y, self.target_x - self.current_x)
        error_angle = desired_angle - current_angle

        # Normalize the angle error to be within -pi to pi
        error_angle = (error_angle + math.pi) % (2 * math.pi) - math.pi
        
        # Proportional control for linear and angular velocity
        # self.linear_vel = self.Kp_linear * distance
        # self.angular_vel = self.Kp_angular * error_angle

        # Proportional control for linear and angular velocity
        self.linear_vel = self.Kp_linear * distance if distance > 0.1 else 0.0
        self.angular_vel = self.Kp_angular * error_angle

        # Apply boundary checks to prevent moving outside the screen
        if self.current_x < self.screen_min_x:
            self.current_x = self.screen_min_x
        elif self.current_x > self.screen_max_x:
            self.current_x = self.screen_max_x

        if self.current_y < self.screen_min_y:
            self.current_y = self.screen_min_y
        elif self.current_y > self.screen_max_y:
            self.current_y = self.screen_max_y

        # Publish Twist message to control TurtleSim
        # twist_msg = Twist()
        # twist_msg.linear = Vector3(linear_vel, 0.0, 0.0)
        # twist_msg.angular = Vector3(0.0, 0.0, angular_vel)
        # self.publisher_cmd.publish(twist_msg)
# -------------------------------------------------------------------

    def callback_turtle_spawner(self, msg):

        self.alive_turtles = msg.name
        self.alive_coordinates = msg.coordinates

        # Update the target to the closest turtle
        if self.alive_coordinates:
            self.other_turtle_vector = self.compute_vectors_for_consecutive_pairs(self.alive_coordinates)
            self.closest = min(self.other_turtle_vector)
            self.index_of_closest_turtle = self.other_turtle_vector.index(self.closest)

            # for cmd_vel and controller (this is Publisher)
            self.target_x = self.alive_coordinates[self.index_of_closest_turtle * 2] # target x position
            self.target_y = self.alive_coordinates[self.index_of_closest_turtle * 2 + 1] # target y position

            # Apply boundary checks to target coordinates
            if self.current_x < self.screen_min_x:
                self.current_x = self.screen_min_x
            elif self.current_x > self.screen_max_x:
                self.current_x = self.screen_max_x

            if self.current_y < self.screen_min_y:
                self.current_y = self.screen_min_y
            elif self.current_y > self.screen_max_y:
                self.current_y = self.screen_max_y
            
            # self.call_catch_turtle_server(self.alive_turtles[self.index_of_closest_turtle])# for request name turtle caught
            if self.current_x > self.target_x - 0.5 and self.current_x < self.target_x + 0.5 and self.current_y > self.target_y - 0.5 and self.current_y < self.target_y + 0.5:
                self.call_catch_turtle_server(self.alive_turtles[self.index_of_closest_turtle])# for request name turtle caught
            
            
            
            # Remove the caught turtle from the lists
            # self.alive_turtles.pop(self.index_of_closest_turtle)
            # self.alive_coordinates.pop(self.index_of_closest_turtle * 2)
            # self.alive_coordinates.pop(self.index_of_closest_turtle * 2 + 1)

# -------------------------------------------------------------------

    # create function to call the server (creat client, create request, call the server, wait for response)
    def call_catch_turtle_server(self, name_turtle_caught):

        #create client for call service.
        client = self.create_client(CatchTurtle, "catch_turtle" )

         #create while loop to waite server on
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Turtle Spawner...")
        
        # create request object
        request = CatchTurtle.Request()
        request.name_turtle_caught = name_turtle_caught

        # send request and get responce in "future" (call server).
        future = client.call_async(request)

        # This will wait until future get response complete.
        # So when future get response complete this will "callback_call_add_two_ints" from "add_done_callback"
        future.add_done_callback(partial(self.callback_call_catch_turtle, name_turtle_caught=name_turtle_caught))

    # process the result in the callback
    def callback_call_catch_turtle(self, future, name_turtle_caught):
        try:
            response = future.result()  #result function is specific to the future object
            self.get_logger().info(f"{name_turtle_caught} was caught!!!")
        except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
            self.get_logger().error("Service call failed %r" % (e, ))

# -------------------------------------------------------------------


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()