#!/usr/bin/env python3
import rospy # type: ignore
from geometry_msgs.msg import Pose2D # type: ignore
import serial # type: ignor

pose = Pose2D()
ser : serial.Serial = None
def connect():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    return ser

def check_data():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split(',')
        pose.x = float(data[0])
        pose.y = float(data[1])
        pose.theta = -1

def talker():
    pub = rospy.Publisher('odometrie', Pose2D, queue_size=10)
    rospy.init_node('odom', anonymous=True)
    rate = rospy.Rate(20) # 10hz
    while not rospy.is_shutdown():
        check_data()
        rospy.loginfo(pose)
        pub.publish(pose)
        rate.sleep()
    
if __name__ == '__main__':
    try:
        connect()
        talker()
    except rospy.ROSInterruptException:
        pass