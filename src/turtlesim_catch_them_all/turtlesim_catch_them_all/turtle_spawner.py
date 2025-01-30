#!/bin/python3
import rclpy
import random
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill # /spawn, /kill
from my_robot_interfaces.msg import Turtle #/name (name alive turtle), /coordinates
from my_robot_interfaces.srv import CatchTurtle
from functools import partial

class TurtleSpawnerNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("turtle_spawner") # MODIFY NAME

        # set parameter
        self.declare_parameter("timer", 1.0)
        # get parameter from the node
        self.timer = self.get_parameter("timer").value

        # create service server
        self.server_ = self.create_service(
            CatchTurtle, "catch_turtle", self.call_back_catch_turtle)

        self.timer = self.create_timer(self.timer, self.spawn_turtle) # Set the timer to call spawn_turtle every 1 seconds
        self.turtle_count = 2  # Starting with turtle2
        self.alive_turtles = []
        self.alive_coordinates = []  # List to store coordinates of alive turtles


        self.data_turtle_alive_publishers_ = self.create_publisher(Turtle, "alive_turtles", 10)
        self.timer_ = self.create_timer(0.01, self.publish_data_turtle_alive)

        self.get_logger().info("Turtle Spawner Node has been stared")

# -------------------------------------------------------------------

    def call_back_catch_turtle(self, request, response):
            
        name_turtle_caught_ = request.name_turtle_caught
        response.name_res = f"{name_turtle_caught_} was caught!!!"

        # remove name turtle caught
        index_name_turtle_caught_ = self.alive_turtles.index(name_turtle_caught_)
        self.alive_turtles.pop(index_name_turtle_caught_)
        # self.alive_turtles.remove(name_turtle_caught_)

        # remove coordinates turtle caught
        self.alive_coordinates.pop(index_name_turtle_caught_)

        self.call_kill_server(name_turtle_caught_)

        return response

# -------------------------------------------------------------------
    def publish_data_turtle_alive(self):
        msg = Turtle()

        msg.name = self.alive_turtles

        # Flatten the list of tuples into a single list of floats
        flattened_coordinates = [coordinate for coordinates in self.alive_coordinates for coordinate in coordinates]
        msg.coordinates = flattened_coordinates
        # msg.coordinates = self.alive_coordinates

        self.data_turtle_alive_publishers_.publish(msg)

# -------------------------------------------------------------------
    def spawn_turtle(self):
        
        x_ = random.uniform(0.0, 11.0)
        y_ = random.uniform(0.0, 11.0)
        name = f"turtle{self.turtle_count}"
        self.turtle_count += 1
        self.call_spawn_server(x_, y_, name)

        

# -------------------------------------------------------------------
    def call_spawn_server(self, x, y, name):
        client = self.create_client(Spawn, "spawn")

        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Turtlesim node...")

        # create request object
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.name = name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn, x=x, y=y, name=name))

    def callback_call_spawn(self, future, x, y, name):
        try:
            response = future.result()  #result function is specific to the future object
            self.alive_turtles.append(name)  # Add the new turtle name to the list
            self.alive_coordinates.append((x, y))  # Add the new turtle coordinates to the list
            # self.get_logger().info(f"{name} has create at x: {x} y: {y} theta: {theta}")
        except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
            self.get_logger().error("Service call failed %r" % (e, ))
# -------------------------------------------------------------------
    def call_kill_server(self, name):
        client = self.create_client(Kill, "kill")

        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Turtlesim node...")

        # create request object
        request = Kill.Request()
        request.name = name

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call_kill, name=name))

    def callback_call_kill(self, future, name):
        try:
            response = future.result()  #result function is specific to the future object
            self.get_logger().info(f"{name} was caught")
        except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
            self.get_logger().error("Service call failed %r" % (e, ))


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()