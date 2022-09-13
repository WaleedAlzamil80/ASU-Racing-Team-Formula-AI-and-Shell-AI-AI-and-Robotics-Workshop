#!/bin/bash

rosservice call spawn "x: 4.5
y: 5.5
theta: 0.0
name: 'turtle2'" 
rosservice call spawn "x: 3.5
y: 5.5
theta: 0.0
name: 'turtle3'" 