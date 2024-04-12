#!/usr/bin/env python3
import rospy # type: ignore
from geometry_msgs.msg import Pose2D # type: ignore
import serial # type: ignore
import serial.tools.list_ports # type: ignore

pose = Pose2D()

def connect():
    print(serial.tools.list_ports.comports()[0].device)
    ser = serial.Serial('/dev/ttyACM0', 9600)
    return ser
    
if __name__ == '__main__':
    try:
        ser = connect()
        rospy.init_node('run_arduino_test', anonymous=True)
        ser.write(b'1')
        while not rospy.is_shutdown(): pass
    except rospy.ROSInterruptException:
        pass