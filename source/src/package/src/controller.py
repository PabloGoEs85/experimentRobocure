#!/usr/bin/env python
#print("Python: controller node")
import rospy
import actionlib
import sys
import random
import time
import os
from threading import Thread
from package.msg import *
from package.srv import *

def sendPersonalityToRobot1(request):
    global personalityRobot1
    personality_profile = personalityRobot1
    return PersonalityResponse(personality_profile)

def sendPersonalityToRobot2(request):
    global personalityRobot2
    personality_profile = personalityRobot2
    return PersonalityResponse(personality_profile)

def sendSentenceToNextRobot(rosClient, sentence):
    goal = SentenceGoal ()

    goal.sentence = sentence
    rosClient.send_goal (goal)

    result = SentenceResult ()
    result.finished = rosClient.wait_for_result ()

def main():
    global personalityRobot1
    global personalityRobot2
    global whoGoesFirst #1 means left / 2 means right
    global startStop #1 starts / 0 stops

    rospy.init_node("controller")
    rospy.wait_for_service('GUICommand')
    try:
        #Gets data from service sent (my case I will need to get responses from questionnaire)
        guiClient = rospy.ServiceProxy ('GUICommand', GUICommand)
        guiCommand = guiClient ()
        personalityRobot1 = guiCommand.command_personality
        personalityRobot2 = (-1)* personalityRobot1
        #personalityRobot2 = personalityRobot1
        whoGoesFirst = guiCommand.command_first
        startStop = guiCommand.command_start

        print "personality robot 1 from gui %d" % personalityRobot1
        print "personality robot 2 from gui %d" % personalityRobot2
        print "who goes first from gui %d" % whoGoesFirst
        print "start from gui %d" % startStop



    except rospy.ServiceException as e:
        print "Service call failed: %s"%e

    #send roles to actuations
    srvControllerToRobot1Server = rospy.Service('controllerPersonality1', Personality, sendPersonalityToRobot1)
    srvControllerToRobot2Server = rospy.Service('controllerPersonality2', Personality, sendPersonalityToRobot2)

    nextRobot = int(whoGoesFirst) #1 --> left, 2 --> right
    #control script
    script = True
    # ... 1. reads from file / gets first sentence (until finished)
    fRobotIntrovert = open('./src/package/src/scriptIntrovert.txt','r')  # opens file with name of "test.txt"
    fRobotExtrovert = open('./src/package/src/scriptExtrovert.txt', 'r')  # opens file with name of "test.txt"

    if(nextRobot == 1 and personalityRobot1 == -1):
        sentence = fRobotIntrovert.readline()
        fakeSentence = fRobotExtrovert.readline ()
    elif (nextRobot == 1 and personalityRobot1 == 1):
        sentence = fRobotExtrovert.readline ()
        fakeSentence = fRobotIntrovert.readline ()
    elif(nextRobot == 2 and personalityRobot2 == -1):
        sentence = fRobotIntrovert.readline()
        fakeSentence = fRobotExtrovert.readline ()
    elif (nextRobot == 2 and personalityRobot2 == 1):
        sentence = fRobotExtrovert.readline ()
        fakeSentence = fRobotIntrovert.readline ()
    if (sentence == ""):
        script = False

    while(script):
        # ... 2. sends sentence to next robot
        rosClient = actionlib.SimpleActionClient('turn'+str(nextRobot), SentenceAction)
        rosClient.wait_for_server ()

        try:
            sendSentenceToNextRobot (rosClient, sentence)
        except KeyboardInterrupt:
            print "Stopping..."
            sys.exit (0)

        # ... 3. waits for feedback
        result = SentenceResult ()
        print "Message received motherfocka CONTROLLER"

        # ... 4. switch to second robot
        nextRobot = (2 - int(whoGoesFirst)) + 1
        whoGoesFirst = nextRobot
        # ... 1. reads from file / gets first sentence (until finished)
        if (nextRobot == 1 and personalityRobot1 == -1):
            sentence = fRobotIntrovert.readline ()
            fakeSentence = fRobotExtrovert.readline ()
        elif (nextRobot == 1 and personalityRobot1 == 1):
            sentence = fRobotExtrovert.readline ()
            fakeSentence = fRobotIntrovert.readline ()
        elif (nextRobot == 2 and personalityRobot2 == -1):
            sentence = fRobotIntrovert.readline ()
            fakeSentence = fRobotExtrovert.readline ()
        elif (nextRobot == 2 and personalityRobot2 == 1):
            sentence = fRobotExtrovert.readline ()
            fakeSentence = fRobotIntrovert.readline ()

        if (sentence == ""):
            script = False

    fRobotIntrovert.close()
    fRobotExtrovert.close ()
    print "This is the end. My friend."
    time.sleep(5) #?
    rospy.spin()


if __name__ == "__main__":
    main()
