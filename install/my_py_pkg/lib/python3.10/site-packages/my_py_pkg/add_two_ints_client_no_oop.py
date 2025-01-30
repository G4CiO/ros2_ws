#!/bin/python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts   #You need to import the service defination(AddTwoInts) same as for the server
                                                # If not the same it will not work

def main(args=None):
    rclpy.init(args=args)
    
    #create node
    node = Node("add_two_ints_no_oop")

    #create client for call service.
    client = node.create_client(AddTwoInts, "add_two_ints", ) # type and name of server should be same as for the server

    #create while loop to waite server on.If no while loop ,when client send request it will fail.
    while not client.wait_for_service(1.0): #after one second, the wait_for_service will exit ,if you not add timeout it will wait forever
        node.get_logger().warn("Waiting for Server Add Two Ints...") 

    # create request object
    request = AddTwoInts.Request()
    request.a = 3
    request.b = 8

    # send request and get responce in "future" (call server).
    future = client.call_async(request) #if use call_async = it will send request, but it wll continue to be executed. Ros team recommend to use
                                        # if use call (syncronous) = it will block until the response is given by the server and sometime it will stuck forever. Ros team not recommend
                                        # future is an object that contains a value that may be set in the future
    
    # this function wait for the response(future) and node, it will spin until future get response complete.
    rclpy.spin_until_future_complete(node, future)



    # if something failed, the future result will has an exception, then you will see error with the reason.
    try:
        response = future.result()  #result function is specific to the future object
        node.get_logger().info(str(request.a) + " + " + str(request.b) + " = " + str(response.sum))
    except Exception as e: #if future result has an exception. (Exception = ข้อยกเว้น)
        node.get_logger().error("Service call failed %r" % (e, ))

    rclpy.shutdown()
    
if __name__=="__main__":
    main()