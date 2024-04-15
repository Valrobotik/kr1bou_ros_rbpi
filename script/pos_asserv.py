import rospy #type: ignore

from geometry_msgs.msg import Pose2D, Twist #type: ignore
import time

def main():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    speed = Twist()
    speed.linear.x = 0.2
    speed.angular.z = 0.2  
    pub.publish(speed)
    time.sleep(3)
    speed.linear.x = 0
    speed.angular.z = 0
    pub.publish(speed)

if __name__ == '__main__':
    try:
        rospy.init_node('pos_asserv', anonymous=True) #node init
        main()
        rospy.spin()   
    except rospy.ROSInterruptException:
        pass