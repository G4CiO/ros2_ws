#!/bin/python3
import rclpy
from rclpy.node import Node

class MyNode(Node): #create class inheriting from Node object
    def __init__(self): #write constructor of the class
        super().__init__("py_test") #call init function from the node and give name of the node
        self.counter_= 0
        self.get_logger().info("Hello Ros2")
        self.create_timer(0.5, self.timer_callback) #print function timer_callback every 2 Hz

    #create timer program
    def timer_callback(self):
        self.counter_ += 1
        self.get_logger().info("Hello " + str(self.counter_))

def main(args=None):
    rclpy.init(args=args)   #initialize Ros2 communication
                            #This is the first line to write in every Ros2 program 
    
    #----------------------------------------------------------
    # node = Node("py_test") #create name of the Node
    # node.get_logger().info("Hello Ros2")    #print "Hello World" in Ros2
                                            #.info is type of text (it have warn,error,etc)
    #----------------------------------------------------------
    node = MyNode() #use oop instead
    
    rclpy.spin(node) #It put the program here, it will run your program until press ctrl c in command line(feel like while loop)
    rclpy.shutdown() #Ros2 communication shutdown and program exit
if __name__=="__main__":
    main()