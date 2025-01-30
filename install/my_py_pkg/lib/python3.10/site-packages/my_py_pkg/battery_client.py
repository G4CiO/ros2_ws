#!/bin/python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLED
from functools import partial

class BatteryNode(Node): 
    def __init__(self):
        super().__init__("battery")

        # first battery is full
        self.call_battery_server(3, "off")

        # Schedule the first call after 4 seconds
        self.timer_on = self.create_timer(4.0, self.call_battery_empty)

    def call_battery_empty(self):
        self.call_battery_server(3, "on")
        # Cancel the timer after it's called
        self.timer_on.cancel()
        # Schedule the next call to turn off the battery after 6 seconds
        self.timer_off = self.create_timer(6.0, self.call_battery_full)

    def call_battery_full(self):
        self.call_battery_server(3, "off")
        # Cancel the timer after it's called
        self.timer_off.cancel()
        # Schedule the next call to turn on the battery after 4 seconds again
        self.timer_on = self.create_timer(4.0, self.call_battery_empty)
        
    def call_battery_server(self, led_number, state):

        #create client for call service.
        battery_client = self.create_client(SetLED, "set_led", )

         #create while loop to waite server on
        while not battery_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Set LED...")
        
        # create request object
        request = SetLED.Request()
        request.led_number = led_number
        request.state = state

        # send request and get responce in "future" (call server).
        future = battery_client.call_async(request)

        # This will wait until future get response complete.
        future.add_done_callback(partial(self.callback_battery_status, 
                                         led_number=led_number, state=state))

    # process the result in the callback
    def callback_battery_status(self, future, led_number, state):
        try:
            response = future.result()  #result function is specific to the future object
            # self.get_logger().info("LED number: "  + str(led_number))
            # self.get_logger().info("State: "  + str(state))
            self.get_logger().info("Success: "  + str(response.success))

            # Log battery status
            if state == "on":
                self.get_logger().info("Battery is empty! Charging battery...")
            elif state == "off":
                self.get_logger().info("Battery is now full again")
                
        except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
            self.get_logger().error("Service call failed %r" % (e, ))


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode() 
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()