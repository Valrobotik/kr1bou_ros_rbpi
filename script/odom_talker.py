#!/usr/bin/env python3
import rospy # type: ignore
from geometry_msgs.msg import Pose2D # type: ignore
import serial
import serial.tools.list_ports

pose = Pose2D()

def connect():
    global ser
    ser = serial.Serial(serial.tools.list_ports.comports()[0].device, 9600)
    return ser

def check_data():
    pub = rospy.Publisher('odometrie', Pose2D, queue_size=10)
    while not rospy.is_shutdown():
        while ser.in_waiting < 1 and not rospy.is_shutdown():
            pass
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            data = line.split(',')

            if(len(data) >= 3):
                try:
                    data[0] = float(data[0]) # position x
                    data[1] = float(data[1]) # position y
                    data[2] = float(data[2]) # angle theta
                    
                    pose.x = data[0]
                    pose.y = data[1]
                    pose.theta = data[2]
                    rospy.loginfo(pose)
                    pub.publish(pose)

                except :
                    rospy.logwarn("Data is not a float")

if __name__ == '__main__':
    try:
        rospy.init_node('odom_talker', anonymous=True)
        connect()
        check_data()

    except rospy.ROSInterruptException:
        pass