#!/usr/bin/env python3
import rospy
import math
import time
from yaml import load
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


def Timer_Callback(event):
    print("Simulation has ended")
    rospy.signal_shutdown('Simulation has ended')

def pose_callback(pose_msg:Pose):
    global x, y, theta
    x = pose_msg.x
    y = pose_msg.y
    theta = pose_msg.theta

def pose_callback1(pose_msg:Pose):
    global x1, y1, theta1
    x1 = pose_msg.x
    y1 = pose_msg.y
    theta1 = pose_msg.theta

def pose_callback2(pose_msg:Pose):
    global x2, y2, theta2
    x2 = pose_msg.x
    y2 = pose_msg.y
    theta2 = pose_msg.theta

def Simulate_Bicycle_Model(v, lr, lf, Delta):
    global Beta,n
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rospy.Timer(rospy.Duration(T), callback = Timer_Callback)

        msg = Twist()
        msg1 = Twist()
        msg2 = Twist()
        
        # Truck
        Beta = math.atan2( lr * math.tan(Delta), (lr+lf) )
        Theta = (v * math.sin(Delta))/(lr + lf)

        msg.linear.x = v
        msg.angular.z = Theta


        #Trailor 1   
        Delta1 = theta - theta1
        v1 = v * math.cos(Delta)
        Theta1 = (v1 * math.sin(Delta1))/(lr + lf)

        msg1.linear.x = v1
        msg1.angular.z = Theta1
        

        #Trailor 2
        Delta2 = theta1 - theta2
        v2 = v1 * math.cos(Delta1)
        Theta2 = (v2 * math.sin(Delta2))/(lr + lf)

        msg2.linear.x = v2
        msg2.angular.z = Theta2


        pub1.publish(msg)
        pub2.publish(msg1)
        pub3.publish(msg2)

        #vx = v * math.cos(Delta + theta)
        #vy = v * math.sin(Delta + theta)
        #msg.linear.y = vy
        #print(vx, vy, Theta)
        #print(Theta, theta)
        #v1x = v1 * math.cos(Delta1 + theta1)
        #v1y = v1 * math.sin(Delta1 + theta1)
        #msg1.linear.y = v1y
        #v2x = v2 * math.cos(Delta2 + theta2)
        #v2y = v2 * math.sin(Delta2 + theta2)
        #msg2.linear.y = v2y

        rate.sleep()
    

if __name__ == "__main__":

        rospy.init_node("Bicycle_Model_Simulator")
        pub1 = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
        pub2 = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size = 10)
        pub3 = rospy.Publisher("/turtle3/cmd_vel", Twist, queue_size = 10)

        sub1 = rospy.Subscriber("/turtle1/pose", Pose, callback = pose_callback)
        sub2 = rospy.Subscriber("/turtle2/pose", Pose, callback = pose_callback1)
        sub3 = rospy.Subscriber("/turtle3/pose", Pose, callback = pose_callback2)
        
        T = int(input("Please enter desired Time of Motion: "))
        v = float(input("Please input linear velocity: "))
        Delta = (float(input("Please enter Steering angle: ")) * math.pi ) / 180
        lf = float(input("Enter the the car’s length from the front wheel to the center of gravity  : "))
        lr = float(input("Enter the the car’s length from the rear wheel to the center of gravity : "))
       
        rospy.loginfo("Simulation has started")
        Simulate_Bicycle_Model(v, lr, lf, Delta)        

