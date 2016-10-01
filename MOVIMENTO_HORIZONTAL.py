#!/usr/bin/python
# coding: utf-8


#----------------------------------------------------------------
# Author: Max Geislinger
# Description: este algoritmo descreve a sétima implementação de OpenCV
# Function: Digital Image -> Transform HSV -> Binary Image -> Erosion Binary -> Find area -> Find Coordinates
# Function 2: Draw circle in centrod (x,y) -> Pins Statemnt -> declaration of motor motion functions -> statement function Z
# Function 3: Perform depth calculation for robot motino
# Tech Libraries: OpenCV, Python, GPIO e NumPy
#---------------------------------------------------------------

import cv2.cv as cv
import cv2 as cv2
import time
import numpy as np
import RPi.GPIO as gpio


gpio.setmode(gpio.BOARD)
# Alerts off
gpio.setwarnings(False)
#---------------------------------------
#Declare pins as GPIO - Motor A
 
#Activating pin for motor A via Rasp 1
gpio.setup(7, gpio.OUT)
 
#Activating pin motor A via Rasp 2 
gpio.setup(11, gpio.OUT)
 
# Start pin 13 as output - Motor A
gpio.setup(13, gpio.OUT)
 
#Start pin 15 as output - Motor A
gpio.setup(15, gpio.OUT)
 
#---------------------------------------
#Declare pins as GPIO - Motor B
 
#pino de ativação do motor B via Rasp 1
gpio.setup(26, gpio.OUT)
 
#pino de ativação do motor B via Rasp 2 
gpio.setup(16, gpio.OUT)
 
# Iniciar Pino 5 como saida - Motor B
gpio.setup(18, gpio.OUT)
 
#Iniciar Pino 22 como saida - Motor B
gpio.setup(22, gpio.OUT)
 


#-----------------------------------------
# Allow L298N is controlled by the GPIO:
#---------------------------------------
#Initial values - True - Motor A ativado
gpio.output(7, True) #Motor A - Rasp 1
gpio.output(11, True) #Motor A - Rasp 2
#---------------------------------------
#initial values - True - Motor B ativado
gpio.output(26, True) #Motor B - Rasp 1
gpio.output(16, True) #Motor B - Rasp 2
#---------------------------------------



# Motor da left
# Padr񥳊# 13 e 15
# F e V -> TrⳊ# V e F -> front
# F e F -> stop

# Motor da right
# 5 e 22
# F e V -> front
# V e F -> TrⳊ# F e F -> stop



def front():
# Motor 1
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)
	
def back():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)
 
 
def stop():
# Motor 1
 gpio.output(18, False)
 gpio.output(22, False)
# Motor 2
 gpio.output(13, False)
 gpio.output(15, False)


def right():
# Motor 1
 gpio.output(13, True)
 gpio.output(15, False)
# Motor 2
 gpio.output(18, True)
 gpio.output(22, False)


def left():
# Motor 1
 gpio.output(13, False)
 gpio.output(15, True)
# Motor 2
 gpio.output(18, False)
 gpio.output(22, True)

 
 def adjustZ(area):
  if(area<=120):
      front()
  elif(area>=600):
      back()
  else:
      stop()
	  
	  
#----------------------------------------------------------------
#    P R O C E S S A M E N T O   D E   I M A G E N S
#------------------------------------------------------------------
# ETAPA 1: OK
# USAR FUNÇÃO INRANGE PARA MUDAR DE RGB-HSV
# PARA ISSO TEMOS QUE DEFINIR OS LIMITES DE VALORES DE H,S E VALORES

# HSV range we use to detect the colored object. 
# In this example, pre-defined for a green ball
#
# HSV Ranges: H: 0-180 , S: 0-255 V: 0-255

#Padrão RED
#Hmin = 0
#Hmax = 179 
#Smin = 131
#Smax = 255
#Vmin = 126
#Vmax = 255

# Yellow Banana
#Hue is around 53
"""
Hmin = 43
Hmax = 63

Smin = 109
Smax = 112

Vmin = 181
Vmax = 211
asdklfjalsk
"""

# Purple Hackathon Bag
Hmin =  140 # 250 /2
Hmax = 	165

Smin = 150
Smax = 160

Vmin = 86
Vmax = 155


 # Creates a HSV array values ​​(minimum and maximum)
rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

# Minimum area to be detected
minArea = 50


#cv.NamedWindow("input")
#cv.NamedWindow("HSV")
#cv.NamedWindow("Thre")
cv.NamedWindow("Erosion")


capture = cv2.VideoCapture(0)

# Parameters capture image of width x height
width = 160
height = 120

# Set a size for the frames (discarding the PyramidDown
if capture.isOpened():
  capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
  capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

  
while True:
    ret, input = capture.read()
    imgHSV = cv2.cvtColor(input,cv2.cv.CV_BGR2HSV)	
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations = 3)
    moments = cv2.moments(imgErode, True)
    area = moments['m00']
    if moments['m00'] >= minArea:
     print(area)
     adjustZ(area)    
    else:
     stop()
    
    cv2.imshow("input",input)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Thre", imgThresh)
    cv2.imshow("Erosion", imgErode)

    if cv.WaitKey(10) == 27:
        break
	cv.DestroyAllWindows()	
	gpio.cleanup()	
	

	
