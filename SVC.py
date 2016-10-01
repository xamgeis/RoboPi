#!/usr/bin/python
# coding: utf-8


#----------------------------------------------------------------
# Autor: Saymon C. A. Oliveira
# Email: saymowan@gmail.com
# DescriÃ§Ã£o: este algoritmo descreve a sexta implementaÃ§Ã£o de OpenCV
# FunÃ§Ãµes: Imagem digital -> TransformaÃ§Ã£o HSV -> Imagem binÃ¡ria -> ErosÃ£o binÃ¡ria -> Encontrar Ã¡rea -> Encontrar coordenadas
# Tecnologias: OpenCV, Python e NumPy
#---------------------------------------------------------------


import cv2.cv as cv
import cv2 as cv2
import time
import numpy as np
import RPi.GPIO as gpio



# Faixa de HSV que usamos para detectar o objeto colorido
# Neste exemplo, prÃ© definidos para uma bola verde
Hmin = 42
Hmax = 92
Smin = 62
Smax = 255
Vmin = 63
Vmax = 235


#PadrÃ£o RED
#Hmin = 0
#Hmax = 179 
#Smin = 131
#Smax = 255
#Vmin = 126
#Vmax = 255


 # Cria-se um array de valores HSV(mÃ­nimo e mÃ¡ximo)
rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

# Ãrea mÃ­nima Ã¡ ser detectada
minArea = 50


cv.NamedWindow("entrance")
cv.NamedWindow("HSV")
cv.NamedWindow("Thre")
cv.NamedWindow("Erosion")


capture = cv2.VideoCapture(0)

# Parametros do tamannho da imagem de captura
width = 160
height = 120

# Definir um tamanho para os frames (descartando o PyramidDown
if capture.isOpened():
  capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
  capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

  
while True:
  ret, entrance = capture.read()
  imgHSV = cv2.cvtColor(entrance,cv2.cv.CV_BGR2HSV)	
  imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
  imgErode = cv2.erode(imgThresh, None, iterations = 3)
  moments = cv2.moments(imgErode, True)
  if moments['m00'] >= minArea:
    x = moments['m10'] / moments['m00']
    y = moments['m01'] / moments['m00']
    print(x, ", ", y)
  cv2.circle(entrance, (int(x), int(y)), 5, (0, 255, 0), -1)

  cv2.imshow("entrance",entrance)
  cv2.imshow("HSV", imgHSV)
  cv2.imshow("Thre", imgThresh)
  cv2.imshow("Erosion", imgErode)

    
	
	
  if cv.WaitKey(10) == 27:
    break
cv.DestroyAllWindows()