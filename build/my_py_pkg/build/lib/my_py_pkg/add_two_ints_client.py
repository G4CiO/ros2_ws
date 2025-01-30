#!/bin/python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial # "partial" allow to add more arguments to our function callback. 

class AddTwoIntsClientNode(Node):
    # You can add publisher,subscriber write your node with other functionalities.

    def __init__(self):
        super().__init__("add_two_ints_client") 
        # initialize a and b
        self.call_add_two_ints_server(6, 7)
        self.call_add_two_ints_server(1, 5)
        self.call_add_two_ints_server(4, 3)

# This part below can use for any of another service client.(like template of service client)
# --------------------------------------------------------------------------------------------------------------
    # create function to call the server (creat client, create request, call the server, wait for response)
    def call_add_two_ints_server(self, a, b):

        #create client for call service.
        client = self.create_client(AddTwoInts, "add_two_ints" )

         #create while loop to waite server on
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server Add Two Ints...")
        
        # create request object
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        # send request and get responce in "future" (call server).
        future = client.call_async(request)

        # This will wait until future get response complete.
        # So when future get response complete this will "callback_call_add_two_ints" from "add_done_callback"
        future.add_done_callback(partial(self.callback_call_add_two_ints, a=a, b=b))

    # process the result in the callback
    def callback_call_add_two_ints(self, future, a, b):
        try:
            response = future.result()  #result function is specific to the future object
            self.get_logger().info(str(a) + " + " + str(b) + " = " + str(response.sum))
        except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
            self.get_logger().error("Service call failed %r" % (e, ))
# --------------------------------------------------------------------------------------------------------------


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientNode() 
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()