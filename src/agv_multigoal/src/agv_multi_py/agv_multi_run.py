#!/usr/bin/env python
import math
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

# Danh sách các mục tiêu định trước
goals = [
   
    # {'x': 2.5, 'y': 0.0, 'z': 0.0, 'w': 1.0},  
    # {'x': 4.5, 'y': 0.0, 'z': math.sqrt(2)/2, 'w': math.sqrt(2)/2},
    # {'x': 4.5, 'y': 1.0, 'z': math.sqrt(2)/2, 'w': math.sqrt(2)/2},
    # {'x': 2.0, 'y': 1.0, 'z': 0.0, 'w': 1.0},

    #{'x': 4.0, 'y': 1.5, 'z': 0.0, 'w': 1.0},
    #{'x': 4.5, 'y': 2.3, 'z': math.sqrt(2)/2, 'w': math.sqrt(2)/2},
   
    {'x': 2.5, 'y': 0.0, 'z': 0.0, 'w': 1.0},            
    {'x': 4.5, 'y': 0.0, 'z': 0.7071, 'w': 0.7071},     
    {'x': 4.5, 'y': 1.4, 'z': 1.0, 'w': 0.0},           
    {'x': 2.0, 'y': 1.4, 'z': 1.0, 'w': 0.0},           
    {'x': 0.1, 'y': 1.4, 'z': math.sqrt(2)/2, 'w': math.sqrt(2)/2},
    {'x': 0.1, 'y': 2.76, 'z': 0, 'w': 1.0},
    {'x': 2.5, 'y': 2.76, 'z': 0, 'w': 1.0},
    {'x': 4.5, 'y': 2.76, 'z': 0, 'w': 1.0},
]

# Hàm tạo mục tiêu gửi tới move_base
def send_goal(x, y, z, w):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w
    return goal

# Hàm điều khiển di chuyển
def move_robot():
    rospy.init_node('multi_goal_navigation')

    # Kết nối tới move_base
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("Đang chờ kết nối tới move_base server...")
    client.wait_for_server()
    rospy.loginfo("Đã kết nối tới move_base server!")

    for idx, goal_coords in enumerate(goals):
        rospy.loginfo(f"Đang gửi mục tiêu {idx + 1}")
        
        # Gửi mục tiêu
        goal = send_goal(goal_coords['x'], goal_coords['y'], goal_coords['z'], goal_coords['w'])
        client.send_goal(goal)
        
        # Đợi mục tiêu hoàn thành hoặc vượt quá thời gian chờ
        finished = client.wait_for_result(rospy.Duration(60))  # Chờ tối đa 60 giây
        if finished:
            rospy.loginfo(f"Mục tiêu {idx + 1} đã hoàn thành!")
        else:
            rospy.logwarn(f"Mục tiêu {idx + 1} không hoàn thành trong thời gian chờ!")

    rospy.loginfo("Tất cả các mục tiêu đã được hoàn thành.")

if __name__ == '__main__':
    try:
        move_robot()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node bị gián đoạn!")