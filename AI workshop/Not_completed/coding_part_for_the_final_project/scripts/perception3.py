#! /bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, Float64MultiArray

trajectory = Twist()
RR = Float64()
RL = Float64()
FR = Float64()
FL = Float64()
pos = Float64MultiArray()
position = np.array([0,0])
Z_prev = Z = 0
waypoints = np.array([0,0])

def callback(recieve):
	global RR,RL,FR,FL,Z,Z_prev
	Z = recieve.linear.z
	
	RR.data = FR.data = -(recieve.linear.x + recieve.angular.z*0.3)
	RL.data = FL.data =  (recieve.linear.x - recieve.angular.z*0.3)
	Z_prev = Z

def gps_call(recieve):
	global pos
	pos[0] = recieve.data[0]
	pos[1] = recieve.data[1]
	

rospy.init_node("control")

rospy.Subscriber("/cmd_vel", Twist, callback)
rospy.Subscriber("/gps", Float64MultiArray, gps_call)

rr = rospy.Publisher("/rear/right_motor",Float64,queue_size = 10)
rl = rospy.Publisher("/rear/left_motor",Float64,queue_size = 10)
fr = rospy.Publisher("/front/right_motor",Float64,queue_size = 10)
fl = rospy.Publisher("/front/left_motor",Float64,queue_size = 10)

while True:

	rr.publish(RR)
	rl.publish(RL)
	fr.publish(FR)
	fl.publish(FL)

	r = rospy.Rate(10)
	r.sleep()

rospy.spin()