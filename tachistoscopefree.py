# Tachistoscope, subliminal video machine
# Roni Bandini, December, 2023
# Free version. MIT License
# For the full version please check https://www.patreon.com/RoniBandini/shop/78990
# bandini.medium.com

import urllib.request
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw, Image
from textwrap import wrap
from openai import OpenAI
import time
from datetime import datetime
from time import sleep
import screeninfo
import requests, json
import RPi.GPIO as GPIO
import tm1637
from youtubesearchpython import VideosSearch
from pytube import YouTube
import random
import os

# 7 segment display
tm = tm1637.TM1637(clk=5, dio=4)

# Gpio
ledPin=2
switchPin=3
butPin=17
gptButPin=27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin,GPIO.OUT)
GPIO.setup(switchPin , GPIO.IN , pull_up_down=GPIO.PUD_UP)
GPIO.setup(butPin , GPIO.IN , pull_up_down=GPIO.PUD_UP)
GPIO.setup(gptButPin , GPIO.IN , pull_up_down=GPIO.PUD_UP)

# Screen calculations
screen_id 	= 0
is_color 	= True
screen 		= screeninfo.get_monitors()[screen_id]
width, height 	= screen.width, screen.height
window_name = 'crt'

# ChatGPT
chatGPTKey      = ""
model           = "text-davinci-003"
prompt          = "Create an indoctrination slogan for a totalitarian state using 4 words or less. Return the slogan only."
temperature     = 0.8

# variables
showInfo="Tom & Jerry show"
showHowManyEpisodes=166
viewedSeconds=0
episode=0
myFramesLimit=1000 # frames limit for new video
mySecondsInsert=5 # insert subliminal frame every x seconds
defaultSlogan="Work hard now"


def writeLog(myLine):
    dt = datetime.now()
    with open('tachistoscope.csv', 'a') as f:
        myLine=str(dt)+","+myLine
        f.write(myLine+"\n")

def getDateAndTime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def writeStats(myStats):
    myStats=str(myStats)
    with open('stats.csv', 'w+') as f:
        f.write(myStats)

def readStats():
    with open("stats.csv", 'r') as f:
        lines = f.readlines()
    myStats=lines[0]
    myStats	= myStats.replace("\n","")
    return myStats


def downloadEpisode():

    global episode
    global showInfo
    global showHowManyEpisodes

    episode = 1

    print("Video download not included in this version")
    writeLog("Video download not included in this version")

def extractFrames():

    global episode
    global myFramesLimit

    print("Removing old frames")

    writeLog("Removing old frames...")

    try:
        os.remove("/frames/*.png")
    except:
        print("No frames to remove")
        writeLog("No frames to remove")


    path="videos/episode"+str(episode)+".mp4"

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    count = 0

    success = 1

    print("Opening video...")
    writeLog("Opening video...")

    while success and count<myFramesLimit:

        success, image = vidObj.read()

        try:
            cv2.imwrite("frames/"+str(count)+".png", image)
        except:
            print("Final frame not saved")

        count += 1

    print("Finished")
    writeLog("All frames saved")

def generateVideo():

    writeLog("Inside...")

    global episode
    global myFramesLimit
    global mySecondsInsert

    img_array = []

    myCounter=1
    myFPS=30
    mySeconds=0

    writeLog("Getting how many frames...")

    lst = os.listdir('frames/')
    number_files = len(lst)

    print ("Source video frames: "+str(number_files))
    writeLog("Frames: "+str(number_files))

    while myCounter<number_files and myCounter<myFramesLimit:

        print("Frame # "+str(myCounter))
        print(str(int(mySeconds))+" seconds")

        if mySeconds>mySecondsInsert:
            myInsertCounter=0
            img = cv2.imread('images/insertframe.png')
            print("* Subliminal frame")

            writeLog("Subliminal frame " +str(myCounter))
            writeLog("Previous size: " +str(width)+"-"+str(height))

            newheight, newwidth, newlayers = img.shape
            newsize = (newwidth,newheight)

            writeLog("Inserted size: "  +str(newwidth)+"-"+str(newheight))

            if (newwidth!=width or newheight!=height):
                # resize image
                writeLog("Resize frame")
                img = cv2.resize(img, size, interpolation = cv2.INTER_AREA)

            mySeconds=0
        else:
            img = cv2.imread('frames/'+str(myCounter)+'.png')

        height, width, layers = img.shape
        size = (width,height)

        img_array.append(img)

        myCounter=myCounter+1
        mySeconds=mySeconds+(1/myFPS)

        fileName="videos/subliminal"+str(episode)+".avi"

    out = cv2.VideoWriter(fileName,cv2.VideoWriter_fourcc(*'DIVX'), myFPS, size)

    print("Saving...")

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()

    print("Subliminal video is ready")

def createAIFrame():

    print("ChatGPT not included in this version")
    writeLog("ChatGPT functions not included in this version")

#######################################################################################################################################


print("Tachistoscope Free Version")
print("@RoniBandini, December 2023")
print("")
tm.write([127, 255, 127, 127])
time.sleep(3)

writeLog("Started")

viewedSeconds=int(readStats())

print(getDateAndTime())
print("Viewed time: "+str(viewedSeconds)+" seconds")

# Load presentation
img = cv2.imread("images/tachistoscope.jpg", cv2.IMREAD_ANYCOLOR)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.imshow(window_name, img)
cv2.waitKey(5000)
tm.number(int(viewedSeconds))


while True:

    # ChatGPT switch led
    if GPIO.input(gptButPin) == GPIO.HIGH:
        GPIO.output(ledPin,GPIO.HIGH)
    else:
        GPIO.output(ledPin,GPIO.LOW)

    if GPIO.input(butPin) == GPIO.LOW:

        print("Download")

        writeLog("Downloading")
        tm.show('down')
        img = cv2.imread("images/downloading.jpg", cv2.IMREAD_ANYCOLOR)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, img)
        cv2.waitKey(1000)
        downloadEpisode()

        writeLog("Extracing")
        tm.show('proc')
        img = cv2.imread("images/processing.jpg", cv2.IMREAD_ANYCOLOR)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, img)
        cv2.waitKey(1000)
        extractFrames()

        # copy source to insert frame just in case it was previously chatgpt based
        os.popen('cp images/insertframesource.png images/insertframe.png')

        if GPIO.input(gptButPin) == GPIO.HIGH:
            writeLog("Generating AI frame")
            tm.show('AI  ')
            img = cv2.imread("images/aislogan.jpg", cv2.IMREAD_ANYCOLOR)
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, img)
            cv2.waitKey(1000)
            createAIFrame()

        writeLog("Inserting frames")
        tm.show('Inse')
        img = cv2.imread("images/inserting.jpg", cv2.IMREAD_ANYCOLOR)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, img)
        cv2.waitKey(1000)
        generateVideo()

        tm.show('done')
        img = cv2.imread("images/ready.jpg", cv2.IMREAD_ANYCOLOR)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, img)
        cv2.waitKey(1000)

    if GPIO.input(switchPin) == GPIO.LOW:

        print("Play On")

        if episode>0:

            # Load subliminal video

            file_name = "videos/subliminal"+str(episode)+".avi"
            window_name = "window"
            interframe_wait_ms = 30

            cap = cv2.VideoCapture(file_name)
            if not cap.isOpened():
                print("Error: Could not open video.")
                writeLog("Could not open video")
                exit()

            tm.show('play')

            cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            start = time.time()
            writeLog("Playing video")

            while (True):
                ret, frame = cap.read()

                if not ret:
                    print("End of video, exiting.")
                    break

                cv2.imshow(window_name, frame)
                if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
                    print("Exit requested.")
                    break

            # calculate seconds, save csv
            end = time.time()
            elapsedSeconds=end - start
            print("Elapsed time: "+str(elapsedSeconds))

            viewedSeconds=viewedSeconds+int(elapsedSeconds)
            tm.number(int(viewedSeconds))
            writeStats(viewedSeconds)
            print("Viewed seconds updated")

            cap.release()
            cv2.destroyAllWindows()
            GPIO.output(ledPin,GPIO.LOW)

            # ReLoad presentation
            img = cv2.imread("images/tachistoscope.jpg", cv2.IMREAD_ANYCOLOR)
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name, img)
            cv2.waitKey(5000)
            tm.number(int(viewedSeconds))

        else:
            print("Please download first")
            tm.show('No')
            time.sleep(3)
            tm.show('vid')
            time.sleep(3)


    time.sleep(1)
