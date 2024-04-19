#!/usr/bin/env python3

import rospy #type: ignore

from geometry_msgs.msg import Pose2D #type: ignore
from std_msgs.msg import Bool #type: ignore
import time

import math

IN_PROGESS = 0
READY = 1

position = Pose2D()

position_camera = Pose2D()
state = READY

starter = Bool

xy = [(1,0), (1, 1), (0, 1), (0, 0)]
def main():
    global pub, objectif,index
    objectif = Pose2D()
    objectif.x = xy[index][0]
    objectif.y = xy[index][1]
    pub.publish(objectif)
    index += 1
    if index >= len(xy):
        index = 0
        
def update_pos(data):
    global position
    #rospy.loginfo(data)
    position = data

def update_starter(data):
    global starter
    starter = data

old_camera_pos = Pose2D()
def update_camera():
    global position_camera, old_camera_pos, corection_odom_pub 
    old_camera_pos = position
    while old_camera_pos == position : pass
    corection_odom_pub.publish(position)


def get_camera(data):
    global position_camera    
    position_camera = data


if __name__ == '__main__':
    try:
        index = 0
        rospy.init_node('pos_asserv', anonymous=True) #node init
        rospy.Subscriber('odometrie', Pose2D, update_pos)
        rospy.Subscriber('starter', Bool, update_starter)
        pub = rospy.Publisher('cmd_mot', Pose2D, queue_size=1)
        corection_odom_pub = rospy.Publisher('odom_correction', Pose2D, queue_size=1)
        time.sleep(1)
        while starter.data == True and not rospy.is_shutdown():
            pass
        update_camera()
        main()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown() and starter.data != True:
            if math.sqrt((position.x - objectif.x)**2 + (position.y - objectif.y)**2) < 0.05:
                update_camera()
                main()
                rospy.loginfo(math.sqrt((position.x - objectif.x)**2 + (position.y - objectif.y)**2))
                rospy.loginfo(f"objectif_x: {objectif.x} objectif_y: {objectif.y}")
                rospy.loginfo(f"position.x: {position.x} position.y: {position.y}")
            rate.sleep()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass