#!/usr/bin/env python3

import rospy #type: ignore

from geometry_msgs.msg import Pose2D, Twist #type: ignore
import time

import math

position = Pose2D()

objectif_x = 0
objectif_y = 0

def main():
    global pub, objectif_x, objectif_y
    pub = rospy.Publisher('cmd_vel', Pose2D, queue_size=10)
    objectif_x = 0.5
    objectif_y = 0.0
    while not rospy.is_shutdown():
        rate = rospy.Rate(10)
        update_moteur(True)
        rate.sleep()

def update_pos(data):
    global position
    position = data

if __name__ == '__main__':
    try:
        rospy.init_node('pos_asserv', anonymous=True) #node init
        rospy.Subscriber('odometrie', Pose2D, update_pos)
        main()
        rospy.spin()   
    except rospy.ROSInterruptException:
        pass