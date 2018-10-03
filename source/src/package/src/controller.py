#!/usr/bin/env python
#print("Python: controller node")
import rospy
import actionlib
import sys
import random
import time
import os
from threading import Thread
#from package.msg import *
from package.srv import *

def sendPersonality(request):
	global personality
	global personality_profile
	#depending on the mode we choose
	#12-26 full introvert; 27-41 slightly introvert; 42-54 ambivert ;55-69 slighlty extrovert ; 70-84 full extrovert
	
	#extraversion + agreeableness
	if (personality <= 26):
		personality_profile = -1.0 #full introvert
	elif (personality <= 41): #slightly introvert
		personality_profile = -0.5
	elif (personality <= 54):
		personality_profile = 0.0 #ambivert
	elif (personality <= 69):
		personality_profile = 0.5 #slightly extrovert
	else:
		personality_profile = 1.0 #full extrovert

	if (flag == 2): #complementary
		if (personality_profile !=0.0):
			personality_profile = personality_profile*(-1)
		else:
			randPersonality = random.randint(1,2) #if 2, it stays as ambivert. If 1, randomizes between fully extrovert or fully introvert
			if (randPersonality == 1):
				randFully = random.randint(1,2)
				if (randFully == 1):
					personality_profile = 1.0 #full extrovert
				else:
					personality_profile = -1.0 #full introvert	
	flag_profile = flag
	#personality_profile = 1.0 #testing purposes

	return PersonalityResponse(personality_profile, flag_profile)

def main():
	global personality
	global flag
	rospy.init_node("controller")
	rospy.wait_for_service('questionnaire')
	try:
		#Gets data from service sent (my case I will need to get responses from questionnaire)
		questionnaireClient = rospy.ServiceProxy('questionnaire', Questionnaire)
		questionnaireToProfile = questionnaireClient()		
		question1 = questionnaireToProfile.q1_response #E1
		question2 = questionnaireToProfile.q2_response #E2
		question3 = 8-questionnaireToProfile.q3_response #E3*
		question4 = questionnaireToProfile.q4_response #E4
		question5 = 8-questionnaireToProfile.q5_response #E5*
		question6 = 8-questionnaireToProfile.q6_response #E6*
		question7 = questionnaireToProfile.q7_response #A1
		question8 = 8-questionnaireToProfile.q8_response #A2*
		question9 = 8-questionnaireToProfile.q9_response #A3*
		question10 = 8-questionnaireToProfile.q10_response #A4*
		question11 = questionnaireToProfile.q11_response #A5
		question12 = questionnaireToProfile.q12_response #A6
		personalityFromGUI = questionnaireToProfile.personality_response 
		flag = questionnaireToProfile.flag_response

	except rospy.ServiceException as e:
		print "Service call failed: %s"%e


	if (personalityFromGUI == 0):
		#compute personality + send profile to actuation and reactive
		extraversion = question1+question2+question3+question4+question5+question6
	#	neuroticism = question2+ question7+question12
	#	openness = question3+question8+question13
	#	conscientiousness = question4+question9+question14
		agreeableness = question7+question8+question9+question10+question11+question12

	#	personality = extraversion + neuroticism + openness + conscientiousness + agreeableness
		personality = extraversion + agreeableness
		print "extraversion %s"%extraversion
		print "agreeableness %s"%agreeableness
	else:
		personality = personalityFromGUI
	print "personality %s"%personality
	print "flag %s"%flag

	#send profile to actuation
	srvAdapterActuationServer = rospy.Service('adapterPersonality', Personality, sendPersonality)

	time.sleep(5)
	rospy.spin()


if __name__ == "__main__":
    main()
