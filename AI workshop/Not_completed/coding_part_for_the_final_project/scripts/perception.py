#!/usr/bin/env python3
from curses import KEY_A1
from enum import Flag
import rospy
import numpy as np
import pcl
from  sensor_msgs.msg import PointCloud2, Image
from std_msgs.msg import Float32MultiArray, Float64
from pynput.keyboard import Listener
import matplotlib.pyplot as plt

gps = np.zeros((2,))             # (1,3)

def gps_callback(msg):
    global gps
    gps[0] = msg.data[0]           # x
    gps[1] = msg.data[1]           # y

point = (gps[0], gps[1])
graph = dict()

y = None
flag = 1

path = []



def zorar1(point):
    global x, graph, flag
    # x = point
    # graph[x] = []

    y = point
    
    if y not in graph.keys():
        graph[y] = []

    graph[x].append(y)
    graph[y].append(x)  
    print(graph)

    x = y


def zorar2(point):
    global x, graph
    min_dist = np.inf
    for key in graph.keys():
        dist = np.sqrt((point[0] - key[0])**2 + (point[1] - key[1])**2)
        if dist < min_dist:
            min_dist = dist
            x = key

def on_release(key):
    global flag, gps, point
    key = str(key)[1]
    if key=='b':
        flag = 0
        listener.stop()
    if key == 'v':
        zorar2((gps[0], gps[1]))
    if key=='q':
        #print(gps[0], gps[1])
        point = (gps[0], gps[1])
        zorar1(point)


# DFS algorithm
def dfs(graph, start, visited=None):
    global path
    if visited is None:
        visited = set()
    visited.add(start)
    path.append(start)
    for next in graph[start]:
        if next not in visited:
            dfs(graph, next, visited)
            path.append(start)



if __name__=="__main__":

    rospy.init_node('go!!!!')

    gps_subscriber = rospy.Subscriber("/gps", Float32MultiArray, callback = gps_callback)
    rospy.sleep(0.1)
    point = (gps[0], gps[1])
    initial_point = point
    x = point        
    graph [x] = []
    print ("initial point", point)
    
    with Listener(on_release=on_release) as listener:
        listener.join()

    visited = set()
    x0 = gps[0]
    y0 = gps[1]
    dfs(graph, initial_point, visited)
    print (path)
    plt.plot(path)

    # arr = np.zeros((len(path),2))
    # for i in range(len(path)):
    #     for j in range(2):
    #         arr[i][j] = path[i][j]
            
    #r = rospy.Rate(10)

    # while not rospy.is_shutdown():
#maybe publish continuously the path we found. ?
    #     # Create msgs to publish ...........#
    #     r.sleep()



