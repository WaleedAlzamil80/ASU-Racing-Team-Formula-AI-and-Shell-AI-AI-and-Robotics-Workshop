#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time
import math

x = 0
y = 0
yaw = 0
t = 0
lr = 0
lf = 0
vel = 0
f_steering = 0
r_steering = 0

def pose_callback(pose_message):
    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def move_with_forward_steering(velocity, forward_steering_angel, interval):

    global yaw, vel, t, lr, lf, f_steering
    f_steering = forward_steering_angel
    vel = velocity
    lr = rospy.get_param("/lr")
    lf = rospy.get_param("/lf")
    t = interval
    velocity_message = Twist()

    start = time.time()
    while(True):

        k = (abs(time.time() - start - t)/t) + 0.1
        beta = math.atan((lr/(lf + lr)) * math.tan(k * f_steering * (math.pi/180)))

        linear_x_speed = vel * math.cos(beta) #* math.cos(yaw + beta)
        #linear_y_speed = vel * math.sin(yaw + beta)
        angular_speed = (vel/(lf + lr)) * math.cos(beta) * math.tan(k * f_steering * (math.pi/180))

        velocity_message.linear.x = linear_x_speed
        #velocity_message.linear.y = linear_y_speed
        velocity_message.angular.z = angular_speed

        publisher.publish(velocity_message)
        if (abs(time.time() - start - t) < 0.1 ):
            break

def move_with_rear_steering(velocity, rear_steering_angel, interval):

    global yaw, vel, t, l, f_steering
    r_steering = rear_steering_angel
    vel = velocity
    lr = rospy.get_param("/lr")
    lf = rospy.get_param("/lf")
    t = interval
    velocity_message = Twist()

    start = time.time()
    while(True):

        k = (abs(time.time() - start - t)/t) + 0.1
        beta = math.atan((lf/(lf + lr)) * math.tan(k * r_steering * (math.pi/180)))
        
        linear_x_speed = vel* math.cos(beta) #* math.cos(yaw - beta)
        #linear_y_speed = vel * math.sin(yaw - beta)
        angular_speed = (vel/(lf + lr)) * math.cos(beta) * math.tan(k * r_steering * (math.pi/180))

        velocity_message.linear.x = linear_x_speed
        #velocity_message.linear.y = linear_y_speed
        velocity_message.angular.z = angular_speed
        
        publisher.publish(velocity_message)
        if (abs(time.time() - start - t) < 0.1 ):
            break

if __name__=="__main__":

    rospy.init_node('Start1')
    publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
    subscriber = rospy.Subscriber("/turtle1/pose", Pose, callback = pose_callback)
    time.sleep(2)

    char = input('For forward Steering press [F] otherwise it will be rear steering : ')

    if char =='F' :
        velocity = float(input("Enter the velocity for the turtlesim : "))
        #lengh_after = float(input("Enter the lengh after the center of gravity : "))
        #lengh_before = float(input("Enter the lengh before the center of gravity : "))
        forward_steering_angel = float(input("Enter the forward steering angle : "))
        interval = float(input("Enter How long do you want your turtle to move : "))
        move_with_forward_steering(velocity , forward_steering_angel, interval)

    else:
        velocity = float(input("Enter the velocity for the turtlesim : "))
        #lengh_after = float(input("Enter the lengh after the center of gravity : "))
        #lengh_before = float(input("Enter the lengh before the center of gravity : "))
        rear_steering_angel = float(input("Enter the rear steering angle : "))
        interval = float(input("Enter How long do you want your turtle to move : "))
        move_with_rear_steering(velocity , rear_steering_angel, interval)
