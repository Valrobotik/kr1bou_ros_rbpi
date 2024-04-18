#!/usr/bin/env python3

import rospy # type: ignore
from geometry_msgs.msg import Pose2D # type: ignore

odometer_value = Pose2D()
camera_value = Pose2D()

def updateOdometry(odom:Pose2D):
    global odometer_value
    odometer_value = odom

def updateCamera(camera:Pose2D):
    global camera_value
    camera_value = camera

def fusion():
    global odometer_value, camera_value
    pub = rospy.Publisher('position', Pose2D, queue_size=1)
    rate = rospy.Rate(20) # 20hz
    while not rospy.is_shutdown():
        # Fusion des données
        result = Pose2D()
        result.x = odometer_value.x         # On prend la valeur de l'odométrie 
        result.y = odometer_value.y         # On prend la valeur de l'odométrie
        result.theta = odometer_value.theta # On prend la valeur de l'odométrie
        rospy.loginfo(result)
        pub.publish(result)
        rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('pos_fusion', anonymous=True)
        rospy.Subscriber('odometrie', Pose2D, updateOdometry)
        rospy.Subscriber('camera', Pose2D, updateCamera)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass

