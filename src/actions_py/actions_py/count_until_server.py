#!/bin/python3
import rclpy
import time
import threading
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import CountUntil
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class CountUntilServerNode(Node): 
    def __init__(self):
        super().__init__("count_until_server")
        self.goal_handle_: ServerGoalHandle = None # **^^$$ goal_handle_ have undefined status (for protect toreject the first goal)
        self.goal_lock_ = threading.Lock() # **^^$$ protect to access variable in different threads(def...) at the same time 
        self.goal_queue_ = [] # $$ create queue goal

        # ---create action server (it will recieved Goal from client)
        self.count_until_server_ = ActionServer(
            self, # node(self)
            CountUntil, # Action type
            "count_until", # Name action server
            goal_callback=self.goal_callback, # It will return accepted or rejected when receive goal
                                              # If return "accepted" then it going to "execute_callback"
                                              # If return "rejected" then it not going to "execute_callback"
            handle_accepted_callback=self.handle_accepted_callback, # for Queue goal (handle goal in ACCEPTED state before reach EXEUTING state)
            cancel_callback=self.cancle_callback, # for cancle goal
            execute_callback=self.execute_callback, # for execute goal
            callback_group=ReentrantCallbackGroup()) # for run Multithreaded executor
        self.get_logger().info("Action server has been started")


    # ---For varidate(ตรวจสอบความถูกต้อง) the arguments(target_number,period) of the goal that client send 
    def goal_callback(self, goal_request: CountUntil.Goal):
        self.get_logger().info("Received a goal")

        # **Policy(นโยบาย): reject new goal if current goal stil active
        # with self.goal_lock_: # for make sure that we don't access the same attribute(varible) in different threads(def) at the same time
            # if self.goal_handle_ is not None and self.goal_handle_.is_active: # check goal_handle_ is not undefined and current goal active
                                                                            # active is mean that the goal not in canceled,succeed,aborted state
                # self.get_logger().info("A goal is already active, rejecting new goal")
                # return GoalResponse.REJECT # reject new goal
        
        # Validate the goal request---Create condition to decide accepted or rejected goal
        if goal_request.target_number < 0:
            self.get_logger().info("Rejecting the goal")
            return GoalResponse.REJECT
        
        # ^^Policy: preempt existing goal(แย่ง goal ที่มีอยู่เดิม) when receiving new goal
        # This policy is after Varlidate because I want to preempt only existing goal that accepted
        # with self.goal_lock_: 
            # if self.goal_handle_ is not None and self.goal_handle_.is_active: # check if first goal is still running(active)
                # self.get_logger().info("Abort current goal and accept new goal")
                # self.goal_handle_.abort() # "abort" the current goal so the goal will not active

        self.get_logger().info("Accepting the goal")
        return GoalResponse.ACCEPT

    # $$ for receive goal to stack in queue
    def handle_accepted_callback(self, goal_handle: ServerGoalHandle):
        with self.goal_lock_:
            if self.goal_handle_ is not None: # if current goal is not undefined
                self.goal_queue_.append(goal_handle) # Add current goal in queue list
            else: # if current goal is undefined
                goal_handle.execute() # this goal will execute directly (no stack in queue) and in execute, goal_handle has been created (goal_handle_ is not None)

    # --Received a cancle request from client
    def cancle_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Received a cancle request")
        # Set state to CANCELING 
        return CancelResponse.ACCEPT # or REJECT
                                     # If ACCEPT, the goal is now in "CANCELING state"

    # ---Recieve Goal
    def execute_callback(self, goal_handle: ServerGoalHandle): # goal_handle = When server receive goal. Server will go to execute_callback and "goal_handle" will receive here
        
        # **^^$$ if there is another thread(def...) that want accessing the goal_handle_, It going to wait until this thread finish in times to times
        with self.goal_lock_: 
            #  check on the current existing(มีอยู่) goal when receive a new goal
            self.goal_handle_ = goal_handle # defined goal_handle_ variable
        
        # Get request from goal
        target_number = goal_handle.request.target_number # target_number is from action interfaces
        period = goal_handle.request.period

        # Execute the action (feedback also here)
        self.get_logger().info("Executing the goal")
        feedback = CountUntil.Feedback() # create feedback object
        result = CountUntil.Result() # create result object
        counter = 0
        for i in range(target_number):
            #^^ Check the current goal is not active when is aborted in Validate step
            if not goal_handle.is_active:
                result.reached_number = counter # send the current result(status,reached_number) that goal aborted
                self.process_next_goal_in_queue() # $$
                return result

            # Check the goal is in "CANCELING state"
            if goal_handle.is_cancel_requested:
                self.get_logger().info("Canceling the goal")
                goal_handle.canceled() # Set goal "canceled" final state (or "succeed" or "aborted")
                result.reached_number = counter # send the current result that goal canceled
                self.process_next_goal_in_queue() # $$
                return result
            counter += 1
            self.get_logger().info(str(counter))
            feedback.current_number = counter # Every time counter increase, feedback will send current number in counter to client
            goal_handle.publish_feedback(feedback) # send feedback to client
            time.sleep(period) # create for counter

        # Once done, set goal final state
        goal_handle.succeed() # Set goal "succeed" final state
        # goal_handle.abort() # Set goal "aborted" final state

        # and send the result
        result.reached_number = counter
        self.process_next_goal_in_queue() # $$
        return result # Return the result
    
    # $$ for process next goal in queue
    # This function use before return result for check do we have another goal in queue?
    def process_next_goal_in_queue(self):
        with self.goal_lock_:
            # Check do we have another goal in the queue
            if len(self.goal_queue_) > 0: # self.goal_queue_ is the lenght of queue
                self.goal_queue_.pop(0).execute() # remove the first element and execute
            else: # when no goal in queue list
                self.goal_handle_ = None # make goal_handle_ to not undefind state for when first goal is come in it woll execute directly

def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServerNode() 
    rclpy.spin(node, MultiThreadedExecutor()) # MultiThreadedExecutor help to spin node multi "def ..._callback()" at the same time
                                              # In this case it help to can spin "cancle_callback" while spin "execute_callback"
    rclpy.shutdown()
    
if __name__=="__main__":
    main()