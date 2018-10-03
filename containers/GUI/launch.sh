#!/bin/bash
source /opt/ros/kinetic/setup.bash

cd /home/rosuser/naoqi/source/
rosdep install actionlib
catkin_make > /dev/null

source ./devel/setup.bash
#echo $PATH
#echo $PYTHONPATH

./src/package/src/gui.py
