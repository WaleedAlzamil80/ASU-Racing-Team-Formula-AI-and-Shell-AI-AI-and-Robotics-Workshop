#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64, Bool
from geometry_msgs.msg import Twist
I_robot = 200*0.057
mass = 200
radius = 0.125
Length = 0.35 

linear_acc = angular_acc = 0.0
k1 = Length/(I_robot * radius)
k2 = 1/(radius * mass)
Tr = Float64()
Tl = Float64()

def update_output(data: Twist):
    global linear_acc, angular_acc, k1,k2,Tr,Tl
    angular_acc = data.angular.z

def update_acceleration(data):
    global linear_acc
    linear_acc = data.data
def update_ebrahim(data):
    global Tl,Tr
    if data.data:
        Tr = 0
        Tl = 0  
        print("Ebrahim is found!!!")


rospy.init_node ('control', anonymous=True)

front_right = rospy.Publisher ('/front/right_motor', Float64, queue_size=10)
front_left = rospy.Publisher ('/front/left_motor', Float64, queue_size=10)
rear_right = rospy.Publisher ('/rear/right_motor', Float64, queue_size=10)
rear_left = rospy.Publisher ('/rear/left_motor', Float64, queue_size=10)

acceleration_subscribe = rospy.Subscriber('/acceleration_module', Float64, update_acceleration)
theta_DD_subscribe = rospy.Subscriber('/theta_module', Twist, update_output)
is_Ebrahim_subscribe = rospy.Subscriber('/is_ebrahim' , Bool, update_ebrahim)


rate = rospy.Rate(100)
while not rospy.is_shutdown():
    Tr.data = 0.25 * (linear_acc/k2 + angular_acc/k1)
    Tl.data = 0.25 * (linear_acc/k2 - angular_acc/k1)    
    # Tr = t2, t4 . Tl = t1, t3

    front_right.publish(Tr)
    front_left.publish(Tl)
    rear_right.publish(Tr)
    rear_left.publish(Tl)
    rate.sleep()