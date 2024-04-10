#!/usr/bin/env python
import rospy # type: ignore
from geometry_msgs.msg import Pose2D # type: ignore

pose = Pose2D()

def check_data():
    pose.x = -1
    pose.y = -1
    pose.theta = -1

def talker():
    pub = rospy.Publisher('odometrie', Pose2D, queue_size=10)
    rospy.init_node('odom', anonymous=True)
    rate = rospy.Rate(20) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(pose)
        pub.publish(pose)
        rate.sleep()
    
if __name__ == '__main__':
    try:
        talker()
        check_data()
    except rospy.ROSInterruptException:
        pass