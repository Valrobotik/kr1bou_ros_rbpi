#!/usr/bin/env python3

import rospy #type: ignore

from geometry_msgs.msg import Pose2D, Twist #type: ignore
from std_msgs.msg import Bool #type: ignore


import serial #type: ignore
import serial.tools.list_ports #type: ignore
import time 

def connect_arduino():
    global ser
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        ser = serial.Serial(p.device, 115200, timeout=0.5)
        ser.write(b'NR')
        rep = str(ser.readline())
        print(rep)
        if "Motor" in rep:
            rospy.loginfo(f'Arduino Motor connected on {p.device}')
            return ser
        rospy.logwarn(f'Arduino Motor not found on {p.device}')
        ser.close()
    raise Exception('Arduino Motor not found') 


def receive_odometry(hey):
    global ser, pub
    position = Pose2D()
    data = str(ser.read_until(b'R')).replace('b', '').replace("'", '').replace('\\r\\n', '').replace('R', '')
    ser.reset_input_buffer()
    print(data)
    data = data.split(';')
    try:
        position.x = float(data[0])
        position.y = float(data[1])
        position.theta = float(data[2])
        #rospy.loginfo(position)
        pub.publish(position)
    except:
        position.x = -1
        position.y = -1
        position.theta = -1
        rospy.logwarn('Data is not a float')
        rospy.logwarn(data)


def send_pos(pos: Pose2D):
    global ser
    rospy.loginfo(f"P{format(pos.x, '.2f')};{format(pos.y, '.2f')}R\n")
    try:
        ser.write(f"P{format(pos.x, '.2f')};{format(pos.y, '.2f')}R\n".encode())
    except:
        rospy.logwarn("Error while sending speed")

def corect_odom(odom: Pose2D):
    global ser
    rospy.loginfo(f"O{odom.x};{odom.y};{odom.theta}R\n")
    try:
        ser.write(f"O{odom.x};{odom.y};{odom.theta}R\n".encode())
    except:
        rospy.logwarn("Error while sending correction")

def emergency_stop(emergency: Bool):
    pass #TODO

def start_motors(x: Bool):
    pass #TODO

if __name__ == '__main__':
    try:
        rospy.init_node('arduino_motor_node', anonymous=True) #node init
        pub = rospy.Publisher('odometrie', Pose2D, queue_size=1)
        ########## subscribe to topic /cmd_vel & /odom_correction ##########
        rospy.Subscriber('cmd_mot', Pose2D, send_pos)
        rospy.Subscriber('odom_correction', Pose2D, corect_odom)
        rospy.Subscriber('emergency', Bool, emergency_stop)
        rospy.Subscriber('starter', Bool, start_motors)

        connect_arduino()
        time.sleep(1)
        curent_odom = Pose2D()
        curent_odom.x = 0.0
        curent_odom.y = 1.0
        curent_odom.theta = 0.12
        #corect_odom(curent_odom)

        rate = rospy.Rate(40)  
        rospy.loginfo('Node started')     
        while not rospy.is_shutdown():
            # do whatever you want here
            if ser.in_waiting > 0:
                receive_odometry(ser)

    except rospy.ROSInterruptException:
        rospy.loginfo('Node killed')

