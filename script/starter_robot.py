#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
import rospy

from std_msgs.msg import Bool

# Lorsque la clé est insérée, le robot envoi à un topic ROS un message indiquant que la clé est insérée (type booléen, True si la clé est insérée, False sinon)
def talker(key):
    pub = rospy.Publisher('starter', Bool, queue_size=10)
    rospy.init_node('starter_talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    is_key_pressed = False
    while not rospy.is_shutdown():
        if key.is_pressed and not is_key_pressed:
            rospy.loginfo(True)
            pub.publish(True)
            is_key_pressed = True
        elif not key.is_pressed and is_key_pressed:
            rospy.loginfo(False)
            pub.publish(False)
            is_key_pressed = False
        rate.sleep()

if __name__ == '__main__':
    key = Button(4)
    try:
        talker(key)
    except rospy.ROSInterruptException:
        pass