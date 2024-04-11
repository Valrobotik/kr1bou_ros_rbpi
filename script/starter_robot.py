from gpiozero import Button
from signal import pause
import rospy

# Lorsque la clé est insérée, le robot envoi à un topic ROS un message indiquant que la clé est insérée (1)
def talker(key):
    pub = rospy.Publisher('starter', int, queue_size=10)
    rospy.init_node('starter_talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if key.is_pressed:
            rospy.loginfo(1)
            pub.publish(1)
        else:
            rospy.loginfo(0)
            pub.publish(0)
        rate.sleep()

if __name__ == '__main__':
    key = Button(4)
    try:
        talker(key)
    except rospy.ROSInterruptException:
        pass