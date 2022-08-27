#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time
import math

x = 0
y = 0
yaw = 0

def pose_callback(pose_message):
    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def go_to_point(X_goal, Y_goal):

    global x, y, yaw
    velocity_message = Twist()

    while(True):
        #K_linear = 0.75
        K_linear = rospy.get_param("/K_linear")
        distance = math.sqrt((X_goal - x)**2 + (Y_goal - y)**2)
        linear_speed = distance * K_linear
        #K_angular = 5
        K_angular = rospy.get_param("/K_angular")
        desired_angle_goal = math.atan2((Y_goal - y),(X_goal - x))
        angular_speed = (desired_angle_goal - yaw)*K_angular
        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        if (distance < 0.02):
            break

def move(speed, distance, is_forward):

    velocity_message = Twist()
    global x,y
    x0 = x
    y0 = y

    if(is_forward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -1*abs(speed)

    distance_moved = 0
    loop_rate = rospy.Rate(10)
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)

    while True :
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distance_moved = math.sqrt((x-x0)**2+ (y-y0)**2)
        print(distance_moved)
        if distance_moved >= distance :
            rospy.loginfo("reached")
            break    
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)

if __name__=="__main__":

    rospy.init_node('Start1')
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
    pose_subscriber = rospy.Subscriber("/turtle1/pose", Pose, callback = pose_callback)
    time.sleep(2)
    x_in = rospy.get_param("/X_goal")
    y_in = rospy.get_param("/Y_goal")
    if ((x > 10)and(y > 10)) or ((x < 1)and(y > 10)) or ((x < 1)and(y < 1)) or ((x > 10)and(y < 1)):
        move(2,1,False)
        go_to_point(x_in,y_in)
    else:
        go_to_point(x_in,y_in)
    
    while True:
        char = input("press [Y] if you want to enter a new position Otherwise it'll exit : ")
        if(char != "Y"):
            break
        x_in = float(input("Enter the x coordinate for the new position : "))
        y_in = float(input("Enter the y coordinate for the new position : "))
        if ((x > 10)and(y > 10)) or ((x < 1)and(y > 10)) or ((x < 1)and(y < 1)) or ((x > 10)and(y < 1)):
            move(2,1,False)
            go_to_point(x_in,y_in)
        else:
            go_to_point(x_in,y_in)

