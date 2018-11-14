#!/bin/bash
source /opt/ros/kinetic/setup.bash

cd /home/rosuser/naoqi/source/
#ls -la
catkin_make > /dev/null

source ./devel/setup.bash
#echo $PATH
#echo $PYTHONPATH

roscore > /dev/null &

#sleep 20s

./src/package/src/actuation.py
#./src/package1/src/cameraSubscriber.py &

#rosrun naoqi_driver naoqi_driver_node --qi-url=tcp://192.168.1.106:9559 --roscore_ip localhost:11311 --network_interface eth0 > /dev/null

#sleep 50s

roslaunch pepper_bringup pepper_full_py.launch nao_ip:=192.168.1.102 > /dev/null

#roslaunch pepper_bringup pepper_full.launch nao_ip:=192.168.1.106 

