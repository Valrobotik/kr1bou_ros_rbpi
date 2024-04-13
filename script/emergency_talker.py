#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
import rospy

from std_msgs.msg import Bool

# Lorsque le bouton d'urgence (Branché sur le GPIO 26) est pressé, le robot envoi à un topic ROS un message indiquant que le bouton d'urgence est pressé (type booléen, True si le bouton d'urgence est pressé, False sinon)
def talker(key):
    pub = rospy.Publisher('emergency', Bool, queue_size=10)
    rospy.init_node('emergency_talker', anonymous=True)
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
    key = Button(26)
    try:
        talker(key)
    except rospy.ROSInterruptException:
        pass