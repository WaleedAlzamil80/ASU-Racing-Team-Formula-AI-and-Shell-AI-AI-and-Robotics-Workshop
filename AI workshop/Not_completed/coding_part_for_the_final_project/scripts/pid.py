#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import  Float32MultiArray
from nav_msgs.msg import Path

current_position = np.zeros((2,1))

def callback(data):
    global current_position
    current_position[0] = data.data[0] #current x position
    current_position[1] = data.data[1] #current y position
    print(current_position)
    
def callback_2(data_2):
    global current_position 
    current_position[2] = data_2.data[0] #current theta

if __name__ == '__main__':

    rospy.init_node ('wheel_inputs')

    way_points = []
    current_position = [0,0,0] #x,y,orientation
    sub_path = Path()
    sub_path = rospy.wait_for_message('/nav_msgs', Path)
    sub_gps = rospy.Subscriber('/gps', Float32MultiArray, callback= callback)
    sub_orientation = rospy.Subscriber('/gyro', Float32MultiArray, callback=callback_2)
    
    pub = rospy.Publisher('theta_module', Twist, queue_size=10)
    r=rospy.Rate(10)
    #PID Parameters
    e_prev = 0
    dt = 0.10
    I = 0
    Kp = 2
    Kd = 0
    Ki = 0


    for i in range (len(sub_path.poses)):
        way_points_x = sub_path.poses[i].pose.position.x
        way_points_y = sub_path.poses[i].pose.position.y
        way_points.append([way_points_x, way_points_y])
    #print(way_points)
    for i in range (len(sub_path.poses)):

        theta_target = np.arctan2(way_points[i][1]-current_position[1], way_points[i][0]-current_position[0])
        distance = np.sqrt((way_points[i][1]-current_position[1])**2 + (way_points[i][0]-current_position[0])**2)

        while (distance < 0.05):
        
            distance = np.sqrt((way_points[i][1]-current_position[1])**2 + (way_points[i][0]-current_position[0])**2)
            
            if(abs(current_position[2] - theta_target) < 0.05 ):
                #Stop the car and turn around
                pub.publish(Twist()) #send a Twist message which is entirely zeroed by default 
                
                # PID calculations
                e = theta_target - current_position[2]

                P = Kp*e
                I = I + Ki*e*dt
                D = Kd*(e - e_prev)/dt


                # update stored data for next iteration
                e_prev = e
                angular_velocity = P + I + D
                msg = Twist()
                msg.angular.z = angular_velocity
                pub.publish(msg) 
            else:
                linear_velocity = 1
                msg_2 = Twist()
                msg_2.linear.x = linear_velocity
                pub.publish(msg_2)
            r.sleep()