#!/bin/env python3
import roslib
import rospy
import math
import tf
from turtlesim.msg import Pose
  
def handle_turtle_pose1(msg: Pose):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta - math.pi/2),
                    rospy.Time.now(),
                    "car1",
                    "world")

def handle_turtle_pose2(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta - math.pi/2),
                    rospy.Time.now(),
                    "car2",
                    "world")

def handle_turtle_pose3(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, msg.theta - math.pi/2),
                    rospy.Time.now(),
                    "car3",
                    "world")
  
if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    #turtlename = rospy.get_param('~turtle')
    sub1 = rospy.Subscriber("/turtle1/pose", Pose, callback =  handle_turtle_pose1)
    sub2 = rospy.Subscriber("/turtle2/pose", Pose, callback =  handle_turtle_pose2)
    sub3 = rospy.Subscriber("/turtle3/pose", Pose, callback =  handle_turtle_pose3)
    rospy.spin()
