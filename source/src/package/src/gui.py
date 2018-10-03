#!/usr/bin/env python2.7
import rospy
from Tkinter import *
from package.srv import *

def launchSystem():
    def sendCommand(command_request):
        global RBpersonality
        global RBwhoFirst

        command_personality = RBpersonality.get()
        command_first = RBwhoFirst.get()
        command_start = 1

        return GUICommandResponse(command_personality, command_first, command_start)

    srvGUIActuationServer = rospy.Service('GUICommand', GUICommand, sendCommand)


#		srvGUIActuationServer = rospy.Service('GUIcommand', StartStop, sendCommand)
#	e12.pack_forget()
#	e12.config(state=status)
#	e12.grid(row=11, column=1)

def main():
    global RBpersonality
    global RBwhoFirst


    rospy.init_node("gui")
    window = Tk ()


    RBpersonality = IntVar()
    RBwhoFirst = IntVar()


    window.title ('Robot Controller')
    widthScreen = window.winfo_screenwidth ()
    heightScreen = window.winfo_screenheight ()
    window.attributes ("-fullscreen", False)  # full screen disavantage:toolbar disappear

    ##### TEXT #####
    frameUpL = Frame (window, width=int (0.2 * widthScreen), height=int (0.2 * heightScreen))
    frameUpL.grid (row=0, column=0)
    frameUpL.pack_propagate (False)

    Radiobutton(frameUpL, variable=RBpersonality, value=1, text="ext vs. int").grid(row=1, column=2)
    Radiobutton(frameUpL, variable=RBpersonality, value=2, text="int vs. ext").grid(row=2, column=2)

    Radiobutton(frameUpL, variable=RBwhoFirst, value=1, text="Left first").grid(row=1, column=4)
    Radiobutton(frameUpL, variable=RBwhoFirst, value=2, text="Right first").grid(row=2, column=4)

    frameDoR = Frame (window, width=int (0.2 * widthScreen), height=int (0.2 * heightScreen))
    frameDoR.grid (row=0, column=1)
    frameDoR.pack_propagate (False)

    ##### BUTTON #####
    button = Button (frameDoR, text="START", font=('', int (15.0 / 768.0 * heightScreen), "bold"), \
                     command=launchSystem, width=int (0.01 * widthScreen), height=int (0.001 * heightScreen))
    button.pack (side="bottom")

    ##### GRAPHICAL INTERFACE + ROBOT BEHAVIOR TOGETHER #####
    window.update_idletasks ()
    window.update ()

    window.mainloop ()

    rospy.spin()

if __name__ == "__main__":
    main ()
