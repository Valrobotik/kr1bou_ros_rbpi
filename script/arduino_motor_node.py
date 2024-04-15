#!/usr/bin/env python3

import rospy #type: ignore

from geometry_msgs.msg import Pose2D, Twist #type: ignore


import serial #type: ignore
import serial.tools.list_ports #type: ignore

def connect_arduino():
    global ser
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        ser = serial.Serial(p.device, 9600)
        ser.write(b'N')
        rep = str(ser.readline())
        print(rep)
        if "Motor" in rep:
            rospy.loginfo(f'Arduino Motor connected on {p.device}')
            return ser
        rospy.logwarn(f'Arduino Motor not found on {p.device}')
        ser.close()
    raise Exception('Arduino Motor not found')


def receive_odometry():
    global ser
    pub = rospy.Publisher('odometrie', Pose2D, queue_size=10)
    position = Pose2D()
    while not rospy.is_shutdown():
        while not rospy.is_shutdown() and ser.in_waiting < 1:
            pass
        data = str(ser.readline()).replace('b', '').replace("'", '').replace('\\r\\n', '')
        data = data.split(',')
        print(data)
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

def send_speed(speed: Twist):
    global ser
    ser.write(f"V{speed.linear.x};{speed.angular.z}\n".encode())
    print(f"V{speed.linear.x};{speed.angular.z}\n")

def corect_odom(odom: Pose2D):
    global ser
    ser.write(f"O{odom.x};{odom.y};{odom.theta}\n".encode())
    print(f"O{odom.x};{odom.y};{odom.theta}\n")


if __name__ == '__main__':
    try:
        rospy.init_node('arduino_motor_node') #node init
        ########## subscribe to topic /cmd_vel & /odom_correction ##########
        rospy.Subscriber('cmd_vel', Twist, send_speed)
        rospy.Subscriber('odom_correction', Pose2D, corect_odom)

        connect_arduino()
        #receive_odometry()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo('Node killed')

