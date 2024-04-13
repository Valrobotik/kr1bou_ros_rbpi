#!/usr/bin/env python3
# license removed for brevity
import rospy
from geometry_msgs.msg import Pose2D # type: ignore

Pose2D()

def talker():
    pub = rospy.Publisher('chatter', Pose2D, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        
        hello_str = Pose2D()
        hello_str.x = 2.1
        hello_str.y = 0.24
        hello_str.theta = 3.14
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass