#!/usr/bin/env python
import rospy
import numpy
from nav_msgs.msg import Odometry
import time

# Biến toàn cục để lưu timestamp lần ghi cuối
(last_logged_time) = None

def callback_odom(data):
    global last_logged_time
    
    # Lấy thời gian hiện tại
    current_time = rospy.Time.now().to_sec()
    
    # Kiểm tra xem đã đủ 0.1 giây từ lần cuối ghi chưa
    if last_logged_time is None or (current_time - last_logged_time >= 0.1):
        last_logged_time = current_time  # Cập nhật thời gian ghi cuối

        # Lấy dữ liệu vị trí (pose) từ odom
        position = data.pose.pose.position
        orientation = data.pose.pose.orientation

        # Ghi dữ liệu vào file
        with open("/home/linh/catkinws3/src/agv_multigoal/src/log/data_odom.txt", "a") as f:
            f.write(f"{current_time}, {position.x:.2f}, {position.y:.2f}, {orientation.z:.2f}, {orientation.w:.2f}\n")
        rospy.loginfo("Ghi dữ liệu odom: x=%f, y=%f", position.x, position.y)

def main():
    rospy.init_node('odom_logger', anonymous=True)
    rospy.Subscriber("/odom", Odometry, callback_odom)
    rospy.loginfo("Node đang ghi dữ liệu odom vào /home/linh/catkinws3/src/agv_multigoal/src/log/data_odom.txt")
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node bị gián đoạn!") 