#!/usr/bin/env python3

import rospy #type: ignore

from geometry_msgs.msg import Pose2D, Twist #type: ignore
import time

import math

IN_PROGESS = 0
READY = 1

POSITION_SHIFT = 0.0

GOTO_BASE_DISTANCE_THRESHOLD = 0.05

WHEEL_FORWARD_SPEED = 0.25
WHEEL_BACKWARD_SPEED = 0.25
WHEEL_TURN_SPEED_FORWARD = 0.3
WHEEL_TURN_SPEED_BACKWARD = 0.3


position = Pose2D()
state = READY

objectif_x = 0
objectif_y = 0
last_left_speed = 0.0
last_right_speed = 0.0

current_speed = Twist()

def AngleDiffRad(a: float, b: float) -> float:
    return math.atan2(math.sin(a - b), math.cos(a - b))

def update_moteur(allow_backward: bool):
    global objectif_x, objectif_y, state, position, last_left_speed, last_right_speed, pub

    state = IN_PROGESS
    x2 = objectif_x
    y2 = objectif_y

    destination_angle = math.atan2(y2 - position.y, x2 - position.x)

    # on shift la position pour ajusté le centre de rotation et le centre de detection
    pos = [position.x, position.y]
    pos[0] -= math.cos(position.theta) * POSITION_SHIFT
    pos[1] -= math.sin(position.theta) * POSITION_SHIFT

    # A GOTO order is defined by a target point (center of a cell) plus a given direction
    p1 = [x2, y2]
    p2 = [x2 + math.cos(destination_angle), y2 + math.sin(destination_angle)]

    # We compute the orthogonal distance between the robot and the target line
    dist_to_line = abs((p2[0] - p1[0]) * (p1[1] - pos[1]) - (p1[0] - pos[0]) * (p2[1] - p1[1])) / math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    # Checking on which side of the target line we are
    angle_line_to_robot = math.atan2(pos[1] - p1[1], pos[0] - p1[0])
    diff_angle_line_to_robot = AngleDiffRad(destination_angle, angle_line_to_robot)
    is_on_right_side = diff_angle_line_to_robot > 0.0
    target_angle = destination_angle + math.atan(dist_to_line * 3.5) * (-1.0 if is_on_right_side else 1.0)  # 7.0

    dx_base = x2 - pos[0]
    dy_base = y2 - pos[1]
    dist_to_base = math.sqrt(dx_base ** 2 + dy_base ** 2)

    state = IN_PROGESS
    m_goto_base_reached = False
    if dist_to_base < GOTO_BASE_DISTANCE_THRESHOLD:
        m_goto_base_reached = True
        state = READY

    angle_diff = AngleDiffRad(target_angle, position.theta)
    backward = abs(angle_diff) > math.pi / 2
    backward = backward and allow_backward
    if backward:
        angle_diff = AngleDiffRad(target_angle + math.pi, position.theta)

    forward_speed = 0.0
    turn_speed = 0.0
    speed_limit = WHEEL_BACKWARD_SPEED if backward else WHEEL_FORWARD_SPEED

    forward_speed = speed_limit * (1.0 - abs(angle_diff) / (math.pi / 2))

    if m_goto_base_reached:
        forward_speed *= 0.1

    if backward:
        forward_speed = -forward_speed

    turn_speed = abs(angle_diff) / (math.pi / 2)
    turn_speed *= WHEEL_TURN_SPEED_BACKWARD if backward else WHEEL_TURN_SPEED_FORWARD
    turn_speed *= 1.0 if angle_diff > 0 else -1.0

    reduction_factor = 1.0
    left_speed = reduction_factor * (forward_speed + turn_speed)
    right_speed = reduction_factor * (forward_speed - turn_speed)

    if state == READY:
        left_speed = 0.0
        right_speed = 0.0

    current_speed.linear.x = left_speed
    current_speed.angular.z = right_speed

    rospy.loginfo(f"Left: {left_speed}, Right: {right_speed}")
    pub.publish(current_speed)

    last_left_speed = left_speed
    last_right_speed = right_speed

def main():
    global pub
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
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