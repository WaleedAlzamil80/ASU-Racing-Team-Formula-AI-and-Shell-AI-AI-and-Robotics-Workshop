#!/usr/bin/env python3
import rospy
import math
import time
from yaml import load
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np

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

        rate.sleep()

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




"""

x1, y1, theta1, theta2, theta3 =0, 0, 0, 0, 0
gps_observation = [x1, x2, theta1, theta2, theta3]

steering = 0
velocity = 0



# Initialize the start values and matrices here
beta = np.arctan(0.5 * np.tan(steering))
Z = np.array([[gps_observation[0]], [gps_observation[1]], [gps_observation[2]], [gps_observation[3]], [gps_observation[4]]])

U_pre = np.array([[0.0], [0.0], [0.0], [0.0], [0.0]])

U = np.array([[0.0], [0.0], [0.0], [0.0], [0.0]])                                                                   # initial state

P_pre = np.array([[0.01, 0.0, 0.0, 0.0, 0.0], [0.0, 0.01, 0.0, 0.0, 0.0], [0.0, 0.0, 0.01, 0.0, 0.0],
            , [0.0, 0.0, 0.01, 0.0, 0.0], [0.0, 0.0, 0.01, 0.0, 0.0]])

H = np.array([[0.01, 0.0, 0.0, 0.0, 0.0], [0.0, 0.01, 0.0, 0.0, 0.0], [0.0, 0.0, 0.01, 0.0, 0.0],
            , [0.0, 0.0, 0.01, 0.0, 0.0], [0.0, 0.0, 0.01, 0.0, 0.0],
             [0.0, 0.01, 0.0, 0.0, 0.0], [0.0, 0.0, 0.01, 0.0, 0.0]])

P = np.array([[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]])                                     # initial uncertainty

F = np.array([[1.0, 0.0, -1.0 * velocity * np.sin(U_pre[2][0] + beta)],                                  # the jaccobian of the state transition function
            [0.0, 1.0, -1.0 * velocity * np.cos(U_pre[2][0] + beta)], 
            [0.0, 0.0, 1.0]])       
  
K = np.array([[0.5, 0.0, 0.0], [0.0, 0.5, 0.0], [0.0, 0.0, 0.5]])                                        # Kalman gain
Q = np.array([[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.001]])                                        # measurement uncertainty
I = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])                                        # identity matrix

########################################
# Implement the kalman filter function 

def kalman_filter(Q = np.array([[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.001]])):
    
    global U, U_pre, P, P_pre, F, K, I , Z

    U_change = np.array([[velocity * np.cos(U_pre[2][0] + beta)], [velocity * np.sin(U_pre[2][0] + beta)], 
                    [U_pre[2][0] + (((velocity/4.9) * np.tan(steering))/(((beta)**2) + 1)**0.5)]])
    U_pre = U
    P_pre = P

    U_pre = U_pre + U_change
    P_pre = np.dot(np.dot(F,P_pre),F.transpose())
    
    K = np.dot(P_pre, np.linalg.inv(P_pre + Q))
    
    U = U_pre + np.dot(K, (Z - U_pre))
    P = np.dot((I - K), P_pre ) """