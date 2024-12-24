#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point, PointStamped
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker, MarkerArray
import tf

# Danh sách các mục tiêu định trước
goals = [
    
    {'x': 2.5, 'y': 0.0},
    {'x': 4.5, 'y': 0.0},
    {'x': 4.5, 'y': 1.4},
    {'x': 2.0, 'y': 1.4},
    {'x': 0.1, 'y': 1.4},
    {'x': 0.1, 'y': 2.76},
    {'x': 2.5, 'y': 2.76},
    {'x': 4.5, 'y': 2.76},
   
   
]

# Danh sách lưu các điểm đã đi qua (dưới frame map)
path_points = []

# Publisher cho MarkerArray
marker_array_pub = None

# Listener TF để chuyển đổi frame
tf_listener = None

# Callback lấy vị trí hiện tại của robot từ /odom
def odom_callback(msg):
    global path_points

    # Lấy vị trí robot trong frame "odom"
    point_in_odom = PointStamped()
    point_in_odom.header.frame_id = "odom"
    point_in_odom.header.stamp = rospy.Time.now()  # Dùng thời gian hiện tại
    point_in_odom.point = msg.pose.pose.position

    try:
        # Chuyển đổi sang frame "map"
        tf_listener.waitForTransform("map", "odom", rospy.Time(0), rospy.Duration(1.0))
        point_in_map = tf_listener.transformPoint("map", point_in_odom)

        # Thêm điểm vào danh sách các điểm đã đi qua
        path_points.append(point_in_map.point)

        # Cập nhật marker
        publish_markers()

    except tf.Exception as ex:
        rospy.logwarn(f"Transform error: {ex}")

# Hàm tạo Marker để hiển thị đường nối các điểm mục tiêu
def create_goal_marker():
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()
    marker.type = Marker.LINE_STRIP
    marker.action = Marker.ADD
    marker.scale.x = 0.05  # Độ dày của đường
    marker.color.a = 1.0
    marker.color.r = 0.0  # Màu đỏ cho đường nối các mục tiêu
    marker.color.g = 1.0
    marker.color.b = 1.0
    marker.id = 0  # ID duy nhất cho marker

    # Thêm các điểm mục tiêu vào marker
    for goal in goals:
        point = Point()
        point.x = goal['x']
        point.y = goal['y']
        point.z = 0.0
        marker.points.append(point)

    return marker

# Hàm tạo Marker để hiển thị đường mà robot đã đi qua
def create_path_marker():
    global path_points
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()
    marker.type = Marker.LINE_STRIP
    marker.action = Marker.ADD
    marker.scale.x = 0.05  # Độ dày của đường
    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 0.0
    marker.color.b = 1.0  # Màu xanh dương cho đường robot đã đi qua
    marker.id = 1  # ID duy nhất cho marker

    z_offset = 0.05  # Offset để đường không bị chìm
    for point in path_points:
        offset_point = Point()
        offset_point.x = point.x
        offset_point.y = point.y
        offset_point.z = point.z + z_offset  # Nâng điểm lên trục z
        marker.points.append(offset_point)

    return marker


# Hàm publish tất cả các marker trong một MarkerArray
def publish_markers():
    global marker_array_pub
    marker_array = MarkerArray()
    
    # Thêm đường nối các mục tiêu
    marker_array.markers.append(create_goal_marker())
    
    # Thêm đường robot đã đi qua
    marker_array.markers.append(create_path_marker())
    
    # Publish MarkerArray
    marker_array_pub.publish(marker_array)

# Node chính
def visualize_path():
    global marker_array_pub, tf_listener
    rospy.init_node('visualize_path')

    # Tạo tf Listener
    tf_listener = tf.TransformListener()

    # Publisher cho MarkerArray
    marker_array_pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10)

    # Subscriber để lấy vị trí robot từ topic /odom
    rospy.Subscriber('/odom', Odometry, odom_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        visualize_path()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node bị gián đoạn!") 