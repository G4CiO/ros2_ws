#!/bin/python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLED
from my_robot_interfaces.msg import LEDPanelState

class LEDPanelNode(Node): 
    def __init__(self):
        super().__init__("led_panel")

        # set parameter
        self.declare_parameter("led_states", [0, 0, 0])
        # get parameter from the node
        self.led_states = self.get_parameter("led_states").value

        # create service server
        self.server_ = self.create_service(
            SetLED, "set_led", self.call_back_led_panel)
        
        self.publishers_ = self.create_publisher(LEDPanelState, "led_states", 10)
        self.timer_ = self.create_timer(1.0, self.publish_led_state)

        # Initialize instance variables
        self.led_number = None
        self.state = None

        self.get_logger().info("Set LED server has been stared.")

    #when send request this callback function will process request and return response.
    def call_back_led_panel(self, request, response):
        # Store request values in instance variables
        self.led_number = request.led_number
        self.state = request.state

        # condition battery status
        if request.led_number == 3 and request.state == "on":
            response.success = True
            self.get_logger().info("Battery status: Empty")
        elif request.led_number == 3 and request.state == "off":
            response.success = True
            self.get_logger().info("Battery status: Full")
        else:
            response.success = False
            self.get_logger().warn("Please key again...")

        return response
    
    def publish_led_state(self):
        msg = LEDPanelState()

        if self.led_number == 3 and self.state == "on":
            msg.led_state = [0, 0, 1]
        elif self.led_number == 3 and self.state == "off":
            msg.led_state = [0, 0, 0]
        else:
            msg.led_state = [-1, -1, -1]
            
        # from parameter
        msg.led_state = self.led_states

        self.publishers_.publish(msg)



def main(args=None):
    rclpy.init(args=args)
    node = LEDPanelNode() 
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()