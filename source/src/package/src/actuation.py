#!/usr/bin/env python
#print("Python: Actuation node")
import rospy
import random
import qi
import sys
import time
import os
#import functools
import actionlib
import threading
from package.msg import *
from package.srv import *

#def play_video(session, url): 
#	try:
#		print("Playing video... " + url)
        #tabletService = session.service("ALTabletService")
        #tabletService.enableWifi()
        #result = tabletService.playVideo(url)
#	except Exception, e:
#		print "Error occured: ", e


#def moveForward(session, speed):
#	x = 1.0
#	y = 0.0
#	theta = 0.0
#	try:
#		print("Moving forwards")
#		moveService = session.service("ALMotion")
#		moveService.moveToward(x, y, theta, [["Frequency", speed]])
#		time.sleep(3)
#		moveService.stopMove()
#	except Exception, e:
#		print "Error occured: ", e
#
#def moveBack(session, speed):
#	x = 1.0
#	y = 0.0
#	theta = -1.0
#	try:
#		print("Moving backwards")
#		moveService = session.service("ALMotion")
#		moveService.moveToward(x, y, theta, [["Frequency", speed]])
#		time.sleep(3)
#		moveService.stopMove()
#	except Exception, e:
#		print "Error occured: ", e
def proxemics(profile, peopleZone1, peopleZone2, peopleZone3):

    moveService = session.service("ALMotion")
    proxemicsService = session.service ("ALMemory")

    if(profile == -1.0):
        if (len (peopleZone1) > 0):
            #idZone1 = str (peopleZone1[0])

            #coordsId1 = proxemicsService.getData ("PeoplePerception/Person/" + idZone1 + "/PositionInRobotFrame")

            x = -0.15
            y = 0.0
            theta = 0.0

            moveService.moveTo(x, y, theta)

    elif(profile == 1.0):
        if (len (peopleZone1) == 0 ):
            if (len (peopleZone2) == 0 ):
                if (len (peopleZone3) > 0 ):
                    idZone3 = str (peopleZone3[0])

                    coordsId3 = proxemicsService.getData ("PeoplePerception/Person/" + idZone3 + "/PositionInRobotFrame")
                    #moveService.setExternalCollisionProtectionEnabled("Move",False)
                    x = 0.2
                    y = (float)(coordsId3[1])/2

                    theta = 0.0
                    moveService.moveTo(x, y, theta)



#speaks with animations
def speak(text, profile):
    global robotSpeaks
    if (profile ==-1.0): #fully introvert
        speed = 80
        volume = 0.5
        pitch = 0.9
    elif (profile == -0.5): #slightly introvert
        speed = 90
        volume = 0.6
        pitch = 0.9
    elif (profile == 0.0): #ambivert
        speed = 95
        volume = 0.65
        pitch = 1.0
    elif (profile == 0.5): #slightly extrovert
        speed = 102
        volume = 0.72
        pitch = 1.0
    elif (profile == 1.0): #fully extrovert
        speed = 90
        volume = 1.0 #0.8
        pitch = 1.1

    try:
        eyeBlinkingBehavior (profile)
        #print("Saying... " + text)
        #sayAnimatedService = session.service("ALAnimatedSpeech")
        sayService = session.service("ALTextToSpeech")

        sayService.setParameter("pitchShift",pitch)
        sayService.setParameter("speed",speed)
        #sayService.resetSpeed()
        sayService.setVolume(volume)
        sayAnimatedService = session.service("ALAnimatedSpeech")

        aux = round(7*random.random ())
        if (profile == 1.0):  # extrovert
            if (aux == 1.0):
                # behavior = "Stand/BodyTalk/Speaking/BodyTalk_1"
                behavior = "Stand/Emotions/Positive/Enthusiastic_1"
            elif (aux == 2.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_2"
            elif (aux == 3.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_3"
            elif (aux == 4.0):
                # behavior = "Stand/BodyTalk/Speaking/BodyTalk_4"
                behavior = "Stand/Emotions/Positive/Optimistic_1"
            elif (aux == 5.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_5"
            elif (aux == 6.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_13"
            else:
                # behavior = "Stand/BodyTalk/Speaking/BodyTalk_14"
                behavior = "Stand/Emotions/Positive/Confident_1"

        elif (profile == 0.0):  # ambivert
            if (aux == 1.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_6"
            elif (aux == 2.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_2"
            elif (aux == 3.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_8"
            elif (aux == 4.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_4"
            elif (aux == 5.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_10"
            elif (aux == 6.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_13"
            else:
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_12"

        elif (profile == -1.0):  # introvert
            if (aux == 1.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_6"
                # behavior = "Stand/Emotions/Neutral/Embarrassed_1"
            elif (aux == 2.0):
                # behavior = "Stand/BodyTalk/Speaking/BodyTalk_7"
                behavior = "Stand/Emotions/Neutral/Innocent_1"
            elif (aux == 3.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_8"
            elif (aux == 4.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_9"
            elif (aux == 5.0):
                # behavior = "Stand/BodyTalk/Speaking/BodyTalk_10"
                #behavior = "Stand/Emotions/Positive/Shy_1"
                behavior = "shybox-b513be/behavior_1"
            elif (aux == 6.0):
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_11"
            else:
                behavior = "Stand/BodyTalk/Speaking/BodyTalk_12"

        text = "^start(" + behavior + ") " + text
        sayAnimatedService.say (text)
        print(text)
        #sayAnimatedService.say("hey there, I'm a social robot")
        facialExpression (0, profile)
        robotSpeaks = True
        eyeBlinkingBehavior(profile)
        robotSpeaks = False
    except Exception as e:
        print "Error occured: ", e


#sets idle motion
def idleMotion(profile, finish):

    motion_service = session.service("ALMotion")
    if(finish == True):
        print "finishing idleMotion"
        motion_service.setIdlePostureEnabled("Body", False)
        motion_service.setIdlePostureEnabled("Arms", False)
        motion_service.setIdlePostureEnabled("Head", False)
    else:

        if(profile == -1.0): #fully introvert
            print "idleMotion fully introvert. Breath"
            motion_service.setBreathEnabled("Body", False)
            motion_service.setBreathEnabled("Arms", True)
            motion_service.setBreathEnabled("Head", False)
        elif(profile == -0.5): #slightly introvert
            print "idleMotion slightly introvert. Breath"
            motion_service.setBreathEnabled("Body", True)
            motion_service.setBreathEnabled("Arms", True)
            motion_service.setBreathEnabled("Head", False)
        elif(profile == 0.0): #ambivert
            print "idleMotion ambivert. Breath"
            motion_service.setBreathEnabled("Body", True)
            motion_service.setBreathEnabled("Arms", True)
            motion_service.setBreathEnabled("Head", True)
        elif(profile == 0.5): #slightly extrovert
            print "idleMotion slightly extrovert. Breath"
            motion_service.setBreathEnabled("Body", True)
            motion_service.setBreathEnabled("Arms", True)
            motion_service.setBreathEnabled("Head", True)
        elif(profile == 1.0): #fully extrovert
            print "idleMotion fully extrovert. Breath"
            motion_service.setBreathEnabled("Body", True)
            motion_service.setBreathEnabled("Arms", True)
            motion_service.setBreathEnabled("Head", True)


#tracks attention
def attentionTracker(profile, finish):
    #trackerService = session.service ("ALTracker")
    #targetName = "Face"
    #faceWidth = 0.1
    #trackerService.registerTarget (targetName, faceWidth)
    #trackerService.track (targetName)

    awarenessService = session.service("ALBasicAwareness")
    if (finish == True):
        print "finishing attentionTracker"
        awarenessService.setEnabled(False) #for naoqi2.5
#		awarenessService.stopAwareness() #naoqi 2.1
        posture_service = session.service("ALRobotPosture")
        posture_service.goToPosture("Crouch", 0.7)
    else:
        if (profile == -1.0): #Fully introvert
            print "attentionTracker fully introvert"
            awarenessService.setParameter("LookStimulusSpeed",0.1)
            awarenessService.setParameter("LookBackSpeed",0.1)
            awarenessService.setStimulusDetectionEnabled("Sound",False)
            awarenessService.setStimulusDetectionEnabled("Movement",False)
            awarenessService.setStimulusDetectionEnabled("NavigationMotion",False)
            awarenessService.setStimulusDetectionEnabled("TabletTouch",False)
            awarenessService.setStimulusDetectionEnabled("Touch",True)
            awarenessService.setStimulusDetectionEnabled("People",True)
            awarenessService.setEngagementMode("FullyEngaged")
            awarenessService.setTrackingMode("Head")
        elif (profile == -0.5): #Slightly introvert
            print "attentionTracker slighlty introvert"
            awarenessService.setParameter("LookStimulusSpeed",0.7)
            awarenessService.setParameter("LookBackSpeed",0.7)
            awarenessService.setStimulusDetectionEnabled("Sound",True)
            awarenessService.setStimulusDetectionEnabled("Movement",False)
            awarenessService.setStimulusDetectionEnabled("NavigationMotion",False)
            awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
            awarenessService.setStimulusDetectionEnabled("Touch",True)
            awarenessService.setStimulusDetectionEnabled("People",True)
            awarenessService.setEngagementMode("FullyEngaged")
            awarenessService.setTrackingMode("BodyRotation")
        elif (profile == 0.0): #Ambivert
            print "attentionTracker ambivert"
            awarenessService.resetAllParameters()
            #awarenessService.setParameter("LookStimulusSpeed",0.5)
            #awarenessService.setParameter("LookBackSpeed",0.5)
            #awarenessService.setStimulusDetectionEnabled("Sound",True)
            #awarenessService.setStimulusDetectionEnabled("Movement",True)
            #awarenessService.setStimulusDetectionEnabled("NavigationMotion",False)
            awarenessService.setStimulusDetectionEnabled("TabletTouch",False)
            #awarenessService.setStimulusDetectionEnabled("Touch",True)
            #awarenessService.setStimulusDetectionEnabled("People",True)
            #awarenessService.setEngagementMode("SemiEngaged")
            #awarenessService.setTrackingMode("BodyRotation")

        elif (profile == 0.5): #Slighlty Extrovert
            print "attentionTracker slighlty extrovert"
            awarenessService.setParameter("LookStimulusSpeed",0.7)
            awarenessService.setParameter("LookBackSpeed",0.7)
            awarenessService.setStimulusDetectionEnabled("Sound",True)
            awarenessService.setStimulusDetectionEnabled("Movement",True)
            awarenessService.setStimulusDetectionEnabled("NavigationMotion",True)
            awarenessService.setStimulusDetectionEnabled("TabletTouch",True)
            awarenessService.setStimulusDetectionEnabled("Touch",True)
            awarenessService.setStimulusDetectionEnabled("People",True)
            awarenessService.setEngagementMode("Unengaged")
            awarenessService.setTrackingMode("BodyRotation")

        elif (profile == 1.0): #Fully Extrovert
            print "attentionTracker fully extrovert"
            awarenessService.setParameter("LookStimulusSpeed",1.0)
            awarenessService.setParameter("LookBackSpeed",1.0)
            #awarenessService.setStimulusDetectionEnabled("Sound",True)
            awarenessService.setStimulusDetectionEnabled ("Sound", False)
            awarenessService.setStimulusDetectionEnabled("Movement",False)
            #awarenessService.setStimulusDetectionEnabled ("Movement", True)
            awarenessService.setStimulusDetectionEnabled("NavigationMotion",True)
            awarenessService.setStimulusDetectionEnabled("TabletTouch",False)
            awarenessService.setStimulusDetectionEnabled("Touch",True)
            awarenessService.setStimulusDetectionEnabled("People",True)
            awarenessService.setEngagementMode("Unengaged")
            awarenessService.setTrackingMode("BodyRotation")
            awarenessService.setTrackingMode("MoveContextually")
            #trackerService.setMode("move")
        awarenessService.setEnabled(True)


#facialExpression
def facialExpression(emotionId, profile):
    facialExpressionService = session.service("ALLeds")
#	facialExpressionService.on("FaceLeds")
    global colorLed
    global faceExpression
    if (emotionId == 1): #happyFace
        colorLed = "green"
    elif (emotionId == 2): #sadFace
        colorLed = "blue"
    elif (emotionId == 0): #neutralFace
        colorLed = "white"
#	elif (emotionId == 3): #angerFace
#		colorLed = "red"
    elif (emotionId == 4): #fearFace
        colorLed = "yellow"

    faceExpression = emotionId
    if(profile == -1.0): #fully introvert
        facialExpressionService.setIntensity("FaceLeds",0.2)
        facialExpressionService.fadeRGB("FaceLeds", colorLed, 1)
        wait = 0.75
    elif(profile == -0.5): #slightly introvert
        facialExpressionService.setIntensity("FaceLeds",0.35)
        facialExpressionService.fadeRGB("FaceLeds", colorLed, 1.25)
        wait = 1
    elif(profile == 0.0): #ambivert
        facialExpressionService.setIntensity("FaceLeds",0.5)
        facialExpressionService.fadeRGB("FaceLeds", colorLed, 1.5)
        wait = 1.25
    elif(profile == 0.5): #slightly extrovert
        facialExpressionService.setIntensity("FaceLeds",0.7)
        facialExpressionService.fadeRGB("FaceLeds", colorLed, 1.75)
        wait = 1.5
    elif(profile == 1.0): #fully extrovert
        facialExpressionService.setIntensity("FaceLeds",0.2)
        facialExpressionService.fadeRGB("FaceLeds", colorLed, 1)
        wait = 2
    #time.sleep(wait)
    colorLed = "white"
    eyeBlinkingBehavior (profile)
    faceExpression = 0
    facialExpressionService.fadeRGB("FaceLeds", colorLed, 1)
    eyeBlinkingBehavior(profile) #as face expression has changed, it needs to update that info


#eye blinking
def eyeBlinkingBehavior(profile):
    global gazeVariation
    global robotEngagedInTask
    global faceExpression
    global faceExpressionPrevious
    global robotSpeaks

    def blinkMorphology():
        def eyeBlinkCommand(duration, fullBlink, blinkType):
            print "About to blink"
            facialExpressionService = session.service("ALLeds")
            facialExpressionService.on("FaceLeds")
            global colorLed #does this work?

            result = facialExpressionService.fadeRGB("FaceLeds", colorLed, 0.0)
            if (result == False):
                print "problem coloring eyes"
            if (fullBlink):
                groupLeds = "FaceLeds"
            else:
                groupLeds = "FaceLedsTop"

            for i in range(blinkType):
                result = facialExpressionService.fadeRGB(groupLeds, 0x000000, duration)
                if (result == False):
                    print "problem coloring eyes"

                #_ledsProxy.fadeRGB(groupLeds, 0x000000, duration / 5. / 1000.); #blinking time shortened by a fourth for NAO as it has no eyelids to move and divided by 1000 to move from milliseconds to seconds
                #_ledsProxy.fadeRGB("FaceLeds", _colorLed, 0.0);
                result = facialExpressionService.fadeRGB("FaceLeds", colorLed, 0.0)
                if (result == False):
                    print "problem coloring eyes"
        duration = 0.0
        aux = random.random()
        if(aux < 0.85): #Single blink
            blinkType = 1
        else:
            aux = random.random()
            if(aux < 0.8): #double blink
                blinkType = 2
            else: #triple blink
                blinkType = 3

        aux = random.random()

        if(aux < 0.91): #Full blink
            fullBlink = True
           #Blink duration with 432ms as mean and 72ms as standard deviation (random number between 360 ms and 504 ms)
            aux2 = random.randint(1,144)/100 # Base (0.36) + a value between the range of [0-144] which is the difference between 504ms and 360ms
            duration = 0.36 + aux2
        else: #half blink
            fullBlink = False
           #Blink duration with 266ms as mean and 4ms as standard deviation (random number between 262 ms and 270 ms)
            aux2 = random.randint(1,8)/100 # Base (0.262) + a value between the range of [0-8] which is the difference between 270ms and 262ms
            duration = 0.262+aux2

        #send eye blinking behavior
        eyeBlinkCommand(duration, fullBlink, blinkType)

    probabilityBlink = 0.0
    numberOcurrences = 0.0
    if(gazeVariation and robotEngagedInTask):
        probabilityBlink += 0.61
        numberOcurrences += 1
        gazeVariation = False

    elif(gazeVariation and not robotEngagedInTask):
        probabilityBlink += 0.72
        numberOcurrences += 1
        gazeVariation=False

    if ((faceExpression != 0)and(faceExpression != faceExpressionPrevious)):
        probabilityBlink += 0.285
        numberOcurrences += 1
        faceExpressionPrevious = faceExpression

    if (robotSpeaks):
        probabilityBlink += 0.31
        numberOcurrences += 1
        robotSpeaks = False

    aux = (numberOcurrences/50)
    if(numberOcurrences > 0):
        probabilityBlink = (probabilityBlink+aux)/(1.75+aux) #Probability normalize between 0 and 1. BlinkingRate = 1.75

    threshold = random.random()

    if (threshold < probabilityBlink):
        blinkMorphology()

    else:
        threshold2 = random.random()
        if(threshold2 > (0.5-(profile/5))):
            blinkMorphology()



def whenTouched(bodyPart): #associates a gesture to the touched body part
    global profileFromController
    facialExpression(1,profileFromController) #happy face
    gesturesService = session.service ("ALBehaviorManager")
    if (bodyPart ==1): #left bumper
        if (profileFromController > -0.1):
            aux = random.random()
            if (aux < 0.33):
                gesture = "Stand/Gestures/BowShort_2"
            elif (aux < 0.66):
                gesture = "Stand/Gestures/BowShort_1"
            else:
                gesture = "Stand/Gestures/BowShort_3"
        else:
            aux2 = random.random()
            if (aux2 < 0.5):
                gesture = "Stand/Gestures/BowShort_1"
            else:
                gesture = "Stand/Gestures/BowShort_3"

    elif (bodyPart ==2): #right bumper
        if (profileFromController > -0.1):
            aux = random.random()
            if (aux < 0.25):
                gesture = "Stand/Gestures/BowShort_2"
            elif (aux < 0.5):
                gesture = "Stand/Gestures/BowShort_1"
            elif (aux < 0.75):
                gesture = "Stand/Reactions/SeeSomething_8"
            else:
                gesture = "Stand/Gestures/BowShort_3"
        else:
            aux2 = random.random()
            if (aux2 < 0.5):
                gesture = "Stand/Gestures/BowShort_1"
            else:
                gesture = "Stand/Gestures/BowShort_3"

    elif (bodyPart == 3): #head
        if (profileFromController > 0.1):
            aux = random.random()
            if (aux < 0.25):
                gesture = "Stand/Reactions/TouchHead_1"
            elif (aux < 0.5):
                gesture = "Stand/Reactions/TouchHead_2"
            elif (aux < 0.75):
                gesture = "Stand/Reactions/TouchHead_3"
            else:
                gesture = "Stand/Reactions/TouchHead_4"
        elif (profileFromController > -0.6):
            aux2 = random.random()
            if (aux2 < 0.33):
                gesture = "Stand/Emotions/Negative/Surprise_1"
            elif (aux2 < 0.66):
                gesture = "Stand/Emotions/Neutral/Innocent_1"
            else:
                gesture = "Stand/Emotions/Negative/Surprise_2"
        else:
            aux2 = random.random()
            if (aux2 < 0.33):
                gesture = "Stand/Emotions/Neutral/Embarrassed_1"
            elif (aux2 < 0.66):
                gesture = "Stand/Emotions/Negative/Hurt_2"
            else:
                gesture = "Stand/Emotions/Positive/Shy_1"
    elif (bodyPart == 4): #left hand
        if (profileFromController < 0.1):
            aux2 = random.random()
            if (aux2 < 0.5):
                gesture = "Stand/Reactions/SeeSomething_5"
            else:
                gesture = "Stand/BodyTalk/Listening/Listening_6"
        else:
            aux2 = random.random()
            if (aux2 < 0.5):
                gesture = "Stand/BodyTalk/Listening/Listening_1"
            else:
                gesture = "Stand/BodyTalk/Listening/Listening_6"

    elif (bodyPart == 5): #right hand
        if (profileFromController > -0.1):
            aux2 = random.random()
            if (aux2 < 0.33):
                gesture = "Stand/BodyTalk/Listening/Listening_2"
            elif (aux2 < 0.66):
                gesture = "Stand/Reactions/SeeSomething_4"
            else:
                gesture = "Stand/BodyTalk/Listening/Listening_6"

        elif (profileFromController > -0.9):
            aux2 = random.random()
            if (aux2 < 0.33):
                gesture = "Stand/Reactions/SeeSomething_5"
            elif(aux2 < 0.66):
                gesture = "Stand/BodyTalk/Listening/Listening_5"
            else:
                gesture = "Stand/BodyTalk/Listening/Listening_6"
        else:
            aux2 = random.random()
            if (aux2 < 0.5):
                gesture = "Stand/Reactions/SeeSomething_6"
            else:
                gesture = "Stand/BodyTalk/Listening/Listening_6"

    result = gesturesService.runBehavior(gesture)
    if (result == False):
        print "running gesture failed"

    facialExpression(0,profileFromController)


def readSensors():
    global finish
    global profileFromController

    peopleService = session.service("ALPeoplePerception")
    peopleService.subscribe("forPeople")

    engagementService = session.service("ALEngagementZones")
    engagementService.subscribe("forEngagement")

    engagementService.setFirstLimitDistance(0.5)
    engagementService.setSecondLimitDistance(2)
    engagementService.setLimitAngle(30)


    try:
        memoryService = session.service("ALMemory")
        #memoryService.raiseEvent("EngagementZones/PersonApproached", "")
        #memoryService.raiseEvent("EngagementZones/PersonMovedAway", "")

    except Exception:
        print "Error when creating memory proxy:"

    while (not finish):

        someoneZone1 = memoryService.getData("EngagementZones/PeopleInZone1")
        someoneZone2 = memoryService.getData("EngagementZones/PeopleInZone2")
        someoneZone3 = memoryService.getData("EngagementZones/PeopleInZone3")
        proxemics (profileFromController, someoneZone1, someoneZone2, someoneZone3)

        leftBumperTouched = 0
        leftBumperTouched = memoryService.getData("LeftBumperPressed")
        if (leftBumperTouched > 0.5):
            whenTouched(1)
            print "Left bumper touched"

        rightBumperTouched = 0
        rightBumperTouched = memoryService.getData("RightBumperPressed")
        if (rightBumperTouched > 0.5):
            whenTouched(2)
            print "Right bumper touched"

        leftHandTouched = 0
        leftHandTouched = memoryService.getData("HandLeftBackTouched")
        if (leftHandTouched > 0.5):
            whenTouched(4)
            print "Left hand touched"

        rightHandTouched = 0
        rightHandTouched = memoryService.getData("HandRightBackTouched")
        if (rightHandTouched > 0.5):
            whenTouched(5)
            print "Right hand touched"

        headTouched = 0
        headFrontTouched = memoryService.getData("FrontTactilTouched")
        headMiddleTouched  = memoryService.getData("MiddleTactilTouched")
        headBackTouched = memoryService.getData("RearTactilTouched")
        if ((headFrontTouched > 0.5)or(headMiddleTouched > 0.5)or(headBackTouched > 0.5)):
            whenTouched(3)
            print "Head touched"


def startIdle():
    global profileFromController

    global faceExpressionPrevious
    global gazeVariation
    global robotEngagedInTask
    global faceExpression
    global robotSpeaks
    global finish
    global colorLed

    colorLed = "white"
    finish = False
    faceExpressionPrevious = 0
    gazeVariation = False
    robotEngagedInTask = False
    faceExpression = 0
    robotSpeaks = False

    posture_service = session.service("ALRobotPosture")
    if (posture_service.getPostureFamily() != "Standing"):
        posture_service.goToPosture("StandInit", 0.25)

    def setIdleBehavior(profile, finishValue):

        attentionTracker(profile, finishValue)
        idleMotion(profile, finishValue)

    #set idle behaviors ON
    setIdleBehavior(profileFromController, finish)

    while(not finish):
        eyeBlinkingBehavior(profileFromController)
        time.sleep(4)

    #set idle behaviors OFF
    setIdleBehavior(profileFromController, finish)



def scriptManager(): #manages the script
    global profileFromController
    def receive_sentence(sentenceSent):

        print "Robot1 " +sentenceSent.sentence

        speak(sentenceSent.sentence, profileFromController)
        time.sleep (1)

        resultSentence = SentenceResult ()
        sentenceServer.set_succeeded (resultSentence)
    # listens to controller to trigger behaviors / speak
    sentenceServer = actionlib.SimpleActionServer ('turn1', SentenceAction,
                                                   receive_sentence, False)
    sentenceServer.start ()


def main(session):
    global finish
    global profileFromController

    rospy.init_node('actuation')

    rospy.wait_for_service('controllerPersonality1') #gets personality for robot1
    try:
        profileClient = rospy.ServiceProxy('controllerPersonality1', Personality)
        profile = profileClient()
        profileFromController = profile.personality_profile

        print "personality for robot 1 %d" %profileFromController

        # sets up personality of the robot
        # ... ?

        tIdle = threading.Thread (target=startIdle)
        tIdle.start ()

        # thread to receive tasks + finish flag from interface
        tScript = threading.Thread (target=scriptManager)
        tScript.start ()

        # thread to listen to sensory information
        tSensorsWhile = threading.Thread (target=readSensors)
        tSensorsWhile.start ()

    except rospy.ServiceException as e:
        print "profile call failed: %s"%e


    rospy.spin()

if __name__ == "__main__":
    try:
        print("Connecting to naoqi...")
        session = qi.Session()
        robotIp = os.environ.get("ROBOT_IP")
        session.connect("tcp://" + robotIp + ":9559")
        print('Connected to naoqi')
    except RuntimeError:
        print ("Cannot connect to naoqi")
    #	sys.exit(1)
    main(session)
