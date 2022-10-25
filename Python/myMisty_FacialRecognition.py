#-----------------------------------------------------------------------------#
# Misty Facial Recognition Skill
# by Phillip Ha 10/22/2019
# Robot Wonderland
# This skill is created to demonstrate the utilization of
# the essential support functions.  They can be used to
# build more advanced skills later
#
# Note: this skill won't drive Misty robot.
# She will perform the skill while being stationary
#
# Support battery level monitoring
# Support head movement control
# Support arm movement control
# Support LED color control
# Support get time of day for greeting
# Support playing audio file
#
# Version: 1.01
#----------------------------------------------------------------------------#
import mistyPy
import time
import sys
from datetime import datetime
import os

# Specify your robot assigned ip address here
robot_IpAddress = "10.94.58.106"
myRobot = mistyPy.Robot(robot_IpAddress)

def battery_check():
    charge_percentage = myRobot.battery()
    print(charge_percentage)
    return float(charge_percentage)

def get_guest_name():
    myRobot.playAudio("Misty_What_is_your_name.wav")
    myRobot.startRecordingAudio("Guest_name.wav")
#    print("Please say your name")
    time.sleep(5)
    myRobot.stopRecordingAudio()
    myRobot.playAudio("Misty_It_is_nice_to_meet_you.wav")
    time.sleep(4)
    # Optional to check guest response
    audio_data = myRobot.getAudioFile("Guest_name.wav")
    myRobot.playAudio(audio_data)


def greeting_time():
    now = datetime.now()
    hnow = now.strftime("%H")
    if(int(hnow) < 12):
        myRobot.playAudio("Misty_Good_morning.wav")
    elif(int(hnow) in range(12,18)):
        myRobot.playAudio("Misty_Good_afternoon.wav")
    else:
        myRobot.playAudio("Misty_Good_evening.wav")

def greeting_name(person_name):
            # Put your trained face names here
            if (person_name == "Steven"):
                myRobot.playAudio("Misty_Hi_Steven.wav")
                myRobot.moveBothArms(5,10,1,1)
                time.sleep(6)
                greeting_time()
            elif (person_name == "Jack"):
                myRobot.playAudio("Misty_Hi_Jack.wav")
                myRobot.moveBothArms(5,10,1,1)
                time.sleep(2)
                greeting_time(6)
            elif (person_name == "Leo"):
                myRobot.playAudio("Misty_Hi_Leo.wav")
                myRobot.moveBothArms(5,10,1,1)
                time.sleep(2)
                greeting_time(6)
            elif (person_name == "Jackie"):
                myRobot.playAudio("austin.m4a")
                myRobot.moveBothArms(5,10,1,1)
                time.sleep(2)
                greeting_time(6)
            elif (person_name == "Grandma"):
                myRobot.playAudio("Misty_Hi_Grandma.wav")
                myRobot.moveBothArms(5,10,1,1)
                time.sleep(2)
                greeting_time(6)
            else:
                myRobot.playAudio("Misty_Hi.wav")
                #get_guest_name()

def FindSomeone():
    myRobot.moveBothArms(5,5,1,1)
    # Let myRobot start some actions
    facefound = False
    myRobot.moveHead(0,0,0)
    # Set a minimum number of face detections to conduct = faces + 1
    faceDetectionLimit = 3
    myRobot.subscribe("FaceRecognition")
    faceview = 1
    nofacecount = 0
    startcounting = False
    face_search_done = False
    foundFaceList = []
    while(face_search_done != True):
        if (faceview % 2):
            myRobot.moveHead(0,1,4,80)
            startcounting = True
        else:
            myRobot.moveHead(0,1,-4,80)
            startcounting = True

        time.sleep(0.25)
        data = myRobot.faceRec()
        if len(data) > 1 and "personName" in data.keys():
            print(data["personName"])
            name      = data["personName"]
            
            # Only greet a recognized person once
            if name not in foundFaceList:
                foundFaceList.append(name)
                greeting_name(name)
                facefound = True
            # scan other direction if needed
            faceview += 1
                
#            face_search_done = True
        else:
            if (startcounting == True):
                nofacecount += 1
            if (nofacecount == 10):
                faceview += 1
                nofacecount = 0
                startcounting = False

        if(faceview > faceDetectionLimit):
            face_search_done = True
            if not facefound:
                myRobot.playAudio("Misty_Hi.wav")
    myRobot.unsubscribe("FaceRecognition")
    myRobot.moveBothArms(5,5,1,1)
    myRobot.moveHead(0,0,0,90)

def main():
    myRobot.printLearnedFaces()
    learnedNameList = myRobot.getLearnedFaces()

    if(len(learnedNameList) == 0):
        print("Please have Misty learn some faces with names assigned.")
    if (battery_check() >= 6.5):
        myRobot.changeLED(0,255,0)
        myRobot.playAudio("I_am_Misty.wav")
        time.sleep(6)
    else:
        myRobot.changeLED(255,0,0)
        myRobot.playAudio("001-OooOooo.wav")

    time.sleep(2)
    robot_info = myRobot.getDeviceInfo()
    hardware_info = robot_info["result"]["hardwareInfo"]
    rtcBoard_info = hardware_info["rtcBoard"]
    print("Misty firmware version: " + rtcBoard_info["firmware"])

    # Let myRobot start some actions
    FindSomeone()

if __name__ == "__main__":
    main()
    os._exit(0)
