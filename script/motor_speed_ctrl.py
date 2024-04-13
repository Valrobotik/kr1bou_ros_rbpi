#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import serial
import serial.tools.list_ports

def connect():
    global ser
    ser = serial.Serial(serial.tools.list_ports.comports()[0].device, 9600)
    return ser

def send_speed(speed:Twist):
    consigne = str(speed.linear.x) + ',' + str(speed.angular.z) + '\n'
    ser.write(consigne.encode())
    rospy.loginfo("send to robot : " + speed)

if __name__ == '__main__':
    try:
        rospy.init_node('motor_speed_ctrl', anonymous=True)
        connect()
        rospy.Subscriber('speed', Twist, send_speed)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass