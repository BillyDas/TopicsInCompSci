from cv2 import *
import numpy as np
import math
import RPi.GPIO as GPIO
import time

# initialize the camera
cam = VideoCapture(2)   # 0 -> index of camera
s, img = cam.read()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

x_origin = None
y_origin = None

x_adjacent = None
y_adjacent = None

pixel_width = 1280
pixel_height = 720

    #Adds a croshair to the image (used to allign the camera)
cv2.line(img,(0,y_origin),(pixel_width,y_origin),(0,255,0),1)
cv2.line(img,(x_origin,0),(x_origin,pixel_height),(0,255,0),1)
cv2.circle(img,(x_origin,y_origin),int(round(y_origin/8,0)),(0,255,0),1)

cv2.imshow("Frame", img)
  