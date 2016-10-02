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
 
#-------------------------------- 
# CONSTANTS
#-------------------------------- 
# Parameters capture of image width x height
width = 160
height = 120

#Horizontal Frame Border
xThresh = width * .3  #threshold is 30% of the border

yThresh = width * .3  #threshold is 30% of the border

# Minimum area to be detected
minArea = 100

# Robot does not move between [followArea , retreatArea] 
followArea = 800 # max area to follow
retreatArea = 2100	# min area to retreat 


#-----------------------------------------
# Allow L298N is controlled by the GPIO:
#---------------------------------------
"""
#Initial values - True - Motor A ativado
gpio.output(7, True) #Motor A - Rasp 1
gpio.output(11, True) #Motor A - Rasp 2
#---------------------------------------
#initial values - True - Motor B ativado
gpio.output(26, True) #Motor B - Rasp 1
gpio.output(16, True) #Motor B - Rasp 2
#---------------------------------------
"""


# Motor da left
# Padr񥳊# 13 e 15
# F e V -> TrⳊ# V e F -> front
# F e F -> stop

# Motor da right
# 5 e 22
# F e V -> front
# V e F -> TrⳊ# F e F -> stop

# Define pins for motors
motorRa = 16 
motorRb = 18
motorRe = 22

motorLa = 36
motorLb = 38
motorLe = 40

gpio.setup(motorRa, gpio.OUT)
gpio.setup(motorRb, gpio.OUT)
gpio.setup(motorRe, gpio.OUT)

gpio.setup(motorLa, gpio.OUT)
gpio.setup(motorLb, gpio.OUT)
gpio.setup(motorLe, gpio.OUT)

def front():
	print "foward"
	gpio.output(motorRa, gpio.HIGH)
	gpio.output(motorRb, gpio.LOW)
	gpio.output(motorRe, gpio.HIGH)

	gpio.output(motorLa, gpio.HIGH)
	gpio.output(motorLb, gpio.LOW)
	gpio.output(motorLe, gpio.HIGH)

def back():
	print "back"
	gpio.output(motorRa, gpio.LOW)
	gpio.output(motorRb, gpio.HIGH)
	gpio.output(motorRe, gpio.HIGH)

	gpio.output(motorLa, gpio.LOW)
	gpio.output(motorLb, gpio.HIGH)
	gpio.output(motorLe, gpio.HIGH)

def stop():
	print "Stopping"
	gpio.output(motorRe, gpio.LOW)
	gpio.output(motorLe, gpio.LOW)


def right():
	print "right"
	# Motor right - stop 
	gpio.output(motorRe, gpio.LOW)

	# Motor left - go foward
	gpio.output(motorLa, gpio.HIGH)
	gpio.output(motorLb, gpio.LOW)
	gpio.output(motorLe, gpio.HIGH)

def left():
	print "left"
	# Motor Right - go foward
	gpio.output(motorRa, gpio.HIGH)
	gpio.output(motorRb, gpio.LOW)
	gpio.output(motorRe, gpio.HIGH)

	# Motor Left - stop
	gpio.output(motorLe, gpio.LOW)



# moves RoboPi away and towards the user 
def adjustZ(area):
	# follow
	if(area<=followArea):
		front()
	# retreat
	elif(area>=retreatArea):
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
Hmin =  109 # 250 /2
Hmax = 	154

Smin = 95
Smax = 204

Vmin = 126
Vmax = 255


 # Creates a HSV array values ​​(minimum and maximum)
rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)



#cv.NamedWindow("input")
#cv.NamedWindow("HSV")
#cv.NamedWindow("Thre")
#cv.NamedWindow("Erosion")


capture = cv2.VideoCapture(0)


# Set a size for the frames (discarding the PyramidDown
if capture.isOpened():
	capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
	capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

  
while True:
	ret, input = capture.read()
	
	input = cv2.GaussianBlur(input,(5,5),0) #apply gaussian blur
	imgHSV = cv2.cvtColor(input,cv2.cv.CV_BGR2HSV)	
	imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
	imgErode = cv2.erode(imgThresh, None, iterations = 3)
	moments = cv2.moments(imgErode, True)
	area = moments['m00']
	if moments['m00'] >= minArea:
		print(area)
		x = moments['m10'] / moments['m00']
		y = moments['m01'] / moments['m00']

		# add green dot for center of object	
		cv2.circle(input, (int(x), int(y)), 5, (0,255,0), -1) 
		#print(x, ", ", y)
		
		#adjust bot horizontal 
		if x < xThresh:
			left()
		elif x > (width - xThresh):
			right()
		else:
			#move bot foward or back	
			adjustZ(area)    
	else:
		#no Area detected, so stop
		stop()

	
	"""
	cv2.imshow("input",input)
	cv2.imshow("HSV", imgHSV)
	cv2.imshow("Thre", imgThresh)
	cv2.imshow("Erosion", imgErode)
	"""
	if cv.WaitKey(10) == 27:
		break

cv.DestroyAllWindows()	
gpio.cleanup()	
