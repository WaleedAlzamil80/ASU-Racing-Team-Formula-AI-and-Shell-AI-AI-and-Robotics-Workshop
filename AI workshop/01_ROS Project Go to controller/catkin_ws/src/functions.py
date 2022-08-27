"""def call_set_pen_service(r, g, b, width, off):

    set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)
    response = set_pen(r, g, b, width, off)"""
"""
    def pose_callback(pose_message):

    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

    f (pose_message.x > 9) or (pose_message.y > 9) or (pose_message.x < 2) or (pose_message.y < 2):
        call_set_pen_service(255, 0, 0, 3, 0)
    else:
        call_set_pen_service(0, 255, 0, 3, 0)"""

"""
    while True :
        #x_in = float(input("Enter the x coordinate for the new position : "))
        #y_in = float(input("Enter the y coordinate for the new position : "))
        x_in = rospy.get_param("/X_goal")
        y_in = rospy.get_param("/Y_goal")
        if ((x > 10)and(y > 10)) or ((x < 1)and(y > 10)) or ((x < 1)and(y < 1)) or ((x > 10)and(y < 1)):
            move(2,1,False)
            go_to_point(x_in,y_in)
        else:
            go_to_point(x_in,y_in)
        char = input("press [Y] if you want to enter a new position Otherwise it'll exit : ")
        if(char != "Y"):
            break"""


"""
previous_x = 0
def call_set_pen_service(r, g, b, width, off):
    try:
        set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)
        response = set_pen(r, g, b, width, off)
        #rospy.loginfo(response)
    except rospy.ServiceException as e:
        rospy.logwarn(e)

def pose_callback(pose:Pose):
    cmd = Twist()
    if pose.x>9 or pose.y>9 or pose.x<2 or pose.y<2 :
        cmd.linear.x = 1.0
        cmd.angular.z = 1.5
    else:
        cmd.linear.x = 5.0
        cmd.angular.z = 0.0
    pub.publish(cmd)

    global previous_x 
    if pose.x >= 5.5 and previous_x < 5.5:
        rospy.loginfo("set color to red")
        call_set_pen_service(255, 0, 0, 3, 0)
    elif pose.x < 5.5 and previous_x >= 5.5:
        rospy.loginfo("set color to green")
        call_set_pen_service(0, 255, 0, 3, 0)
    previous_x = pose.x

def rotate(angular_speed_degree, relative_angle_degree, clockwise):
    global yaw
    velocity_message = Twist()
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0
    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    theta0 = yaw
    angular_speed = math.radians(abs(angular_speed_degree))
    if(clockwise):
        velocity_message.angular.z = abs(angular_speed)
    else:
        velocity_message.angular.z = -1 * abs(angular_speed)
    angle_moved = 0.0
    loop_rate = rospy.Rate(10)
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
    t0 = rospy.Time.now().to_sec()
    while True:
        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        current_angel_degree = (t1 - t0)*angular_speed_degree
        loop_rate.sleep()
        if(current_angel_degree>=relative_angle_degree):
            rospy.loginfo("reached")
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)
    """
