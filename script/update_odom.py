#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose2D
import serial
import serial.tools.list_ports

def connect():
    global ser
    ser = serial.Serial(serial.tools.list_ports.comports()[0].device, 9600)
    return ser

def update_odom(speed:Pose2D):
    new_odom = 'O' + str(speed.x) + ',' + str(speed.y) + ',' + str(speed.theta) + '\n'
    ser.write(new_odom.encode())
    rospy.loginfo("send to robot : " + speed)

if __name__ == '__main__':
    try:
        rospy.init_node('update_odom', anonymous=True)
        connect()
        rospy.Subscriber('new_odom', Pose2D, update_odom)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass