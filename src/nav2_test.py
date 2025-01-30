#!/bin/python3
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped   # This for send initial pose to the BasicNavigator
                                            # and BasicNavigator will send your initial pose message to initial_pose topic
import tf_transformations

def create_pose_stamped(navigator: BasicNavigator, position_x, position_y, orientation_z):
    # This is for compute angle to euler angle
    q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z) #orentation radian angle (x, y, z)
    
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()

    # Incase Initial_pose this pose reference from /map
    pose.pose.position.x = position_x
    pose.pose.position.y = position_y
    pose.pose.position.z = 0.0
    
    #  Default is Quaternions angle
    pose.pose.orientation.x = q_x
    pose.pose.orientation.y = q_y
    pose.pose.orientation.z = q_z
    pose.pose.orientation.w = q_w

    return pose

def main():
    # --- Init
    rclpy.init()
    nav = BasicNavigator() # nav = Nav2 in ros2

    # --- Set initial pose (for give a pose stamped object to the BasicNavigator)
    initial_pose = create_pose_stamped(nav, 0.0, 0.0, 0.0)
    nav.setInitialPose(initial_pose)   # Comment this line if you want set goal again by not close gazebo   

    # ---Wait for Nav2
    nav.waitUntilNav2Active()

    # --- Send Nav2 goal
    goal_pos1 = create_pose_stamped(nav, 3.5, 1.0, 1.57)
    goal_pos2 = create_pose_stamped(nav, 2.0, 2.5, 3.14)
    goal_pos3 = create_pose_stamped(nav, 0.5, 1.0, -1.57)

    # --- Go to one pose
    # nav.goToPose(goal_pos1)
    # --- Wait goToPose() send goal pose to Nav2 complete or position have been "reached" or "aborted" (It will be True)
    # while not nav.isTaskComplete():
        # pass
        # This below is noncessaly for this while loop
        #feedback = nav.getFeedback() # It will give current position of robot
        #print(feedback)

    # --- Follow waypoints
    waypoint = [goal_pos1, goal_pos2, goal_pos3]
    # for i in range(3): #it for you want to set this waypointby loop (In this case is 3 round)
    nav.followWaypoints(waypoint)
    while not nav.isTaskComplete():
        pass

    # --- Show result of robot to terminal (example of result: SUCCEEDED, ABORTED)
    print(nav.getResult())

    # --- Shutdown
    rclpy.shutdown()

if __name__ == '__main__':
    main()