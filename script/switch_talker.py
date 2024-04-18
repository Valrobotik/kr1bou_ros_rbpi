#!/usr/bin/env python3
# switch_talker.py
# SWITCH TALKER NODE


from gpiozero import Button
from signal import pause
import rospy

from std_msgs.msg import Byte

sw1_state = False
sw2_state = False
sw3_state = False
sw4_state = False

# Lorsque la clé est insérée, le robot envoi à un topic ROS un message indiquant que la clé est insérée (type booléen, True si la clé est insérée, False sinon)
def talker():
    pub = rospy.Publisher('switch', Byte, queue_size=10)
    rate = rospy.Rate(20) # 20hz
    
    sw1 = Button(0)
    sw2 = Button(1)
    sw3 = Button(5)
    sw4 = Button(6)

    sw1_state = sw1.is_not_pressed
    sw2_state = sw2.is_not_pressed
    sw3_state = sw3.is_not_pressed
    sw4_state = sw4.is_not_pressed

    while not rospy.is_shutdown():
        if (sw1.is_pressed and not sw1_state) or (sw2.is_pressed and not sw2_state) or (sw3.is_pressed and not sw3_state) or (sw4.is_pressed and not sw4_state) or  (not sw1.is_pressed and sw1_state) or (not sw2.is_pressed and sw2_state) or (not sw3.is_pressed and sw3_state) or (not sw4.is_pressed and sw4_state):
            sw1_state = sw1.is_pressed
            sw2_state = sw2.is_pressed
            sw3_state = sw3.is_pressed
            sw4_state = sw4.is_pressed

            result = Byte()
            result.data = 0
            if sw1_state:
                result.data += 1
            if sw2_state:
                result.data += 2
            if sw3_state:
                result.data += 4
            if sw4_state:
                result.data += 8

            rospy.loginfo(result)
            pub.publish(result)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('switch_talker', anonymous=True)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass