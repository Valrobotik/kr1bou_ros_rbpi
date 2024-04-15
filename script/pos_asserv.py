#!/usr/bin/env python3

import rospy #type: ignore

from geometry_msgs.msg import Pose2D #type: ignore
import time

import math

IN_PROGESS = 0
READY = 1

position = Pose2D()
state = READY

objectif_x = 0
objectif_y = 0

xy = [(0.5, 0.0), (0.5, 0.5), (0.0, 0.5), (0.0, 0.0)]
def main():
    global pub, objectif_x, objectif_y,index
    objectif = Pose2D()
    objectif.x = xy[index][0]
    objectif.y = xy[index][1]
    pub.publish(objectif)
    index += 1
    if index >= len(xy):
        index = 0
        
def update_pos(data):
    global position
    rospy.loginfo(data)
    position = data

if __name__ == '__main__':
    try:
        index = 0
        rospy.init_node('pos_asserv', anonymous=True) #node init
        rospy.Subscriber('odometrie', Pose2D, update_pos)
        pub = rospy.Publisher('cmd_mot', Pose2D, queue_size=10)
        time.sleep(1)
        main()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if math.sqrt((position.x - objectif_x)**2 + (position.y - objectif_y)**2) < 0.05:
                main()
            rate.sleep()
        rospy.spin()

    except rospy.ROSInterruptException:
        pass