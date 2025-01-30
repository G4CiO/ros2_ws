#!/bin/python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import CountUntil

class CountUntilClientNode(Node):
    def __init__(self):
        super().__init__("count_until_client")
        # create action client (for send goal to server)
        self.count_until_client_ = ActionClient(self, CountUntil, "count_until") # Should same type and name with server
    
    def send_goal(self, targer_number, period):
        # Wait for the server before send goal to server
        self.count_until_client_.wait_for_server()

        # Create a goal
        goal = CountUntil.Goal()
        goal.target_number = targer_number
        goal.period = period

        # Send the goal
        self.get_logger().info("Sending goal") # if use send_goal() instead send_goal_async() it will block code and not reach spin node
        self.count_until_client_. \
            send_goal_async(goal, feedback_callback=self.goal_feedback_callback). \
                add_done_callback(self.goal_response_callback)  # send goal and have future
                                                                # add_done_callback() call when the future is finished
                                                                #  \ for go to new line
        
        # Example for send cancel request---Send a cancle request 2 seconds later
        # self.timer_ = self.create_timer(2.0, self.cancel_goal)

    def cancel_goal(self):
        self.get_logger().info("Send a cancle request")
        self.goal_handle_.cancel_goal_async() # Send a cancle request
        self.timer_.cancel()
                                                        
    # receive response goal from server that accepted or rejected
    def goal_response_callback(self, future):
        self.goal_handle_: ClientGoalHandle = future.result()
        if self.goal_handle_.accepted: # check if the goal have been accepted by server we will send request for the result
            self.get_logger().info("Goal got accepted")
            # send request for the result(get_result_async) and get the future(add_done_callback)
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            # No send request for the result because it no result in server if rejected
            self.get_logger().warn("Goal got rejected")

    
    # This callback will work when the result is received 
    # get response from server for the result
    def goal_result_callback(self, future):
        status = future.result().status
        # get the result of the future
        result = future.result().result # Now "result" have "reached_number"
        # Check status of goal from server
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        # show result from future(server) on turminal (Whatever Success or Aborted it still get result)
        self.get_logger().info("Result: " + str(result.reached_number))

    # subcribed feedback from server everytime when "send_goal_async" work in "Send the goal"
    def goal_feedback_callback(self, feedback_msg):
        number = feedback_msg.feedback.current_number
        self.get_logger().info("Got feedback: " + str(number))
                                                                         

def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClientNode()
    # send goal
    node.send_goal(5, 1.0)
    # send multiple goals and run them in parallel
    # node.send_goal(6, 0.5)
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__=="__main__":
    main()