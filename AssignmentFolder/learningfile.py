import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#27 LED
left_Stopper = 6
Right_Stopper = 5
#28 Switch

GPIO.setup(left_Stopper, GPIO.IN)
GPIO.setup(Right_Stopper, GPIO.IN)
left = 1
right = 0

def readinput():
    global LSwitchIsOn
    global RSwitchIsOn
    LSwitchIsOn = GPIO.input(left_Stopper)
    RSwitchIsOn = GPIO.input(Right_Stopper)


while 1:
    if left == 1:
        while left == 1:
            readinput()
            if LSwitchIsOn == 1:
                print("RED CLICKED")
                time.sleep(.10)
                left = 0
                right = 1
            elif LSwitchIsOn == 0:
                print("RED NOT CLICKED")
                time.sleep(.10)
    elif right == 1:
        while right == 1:
            readinput()
            if RSwitchIsOn == 1:
                print("GREEN CLICKED")
                time.sleep(.10)
                left = 1
                right = 0
            elif RSwitchIsOn == 0:
                print("GREEN NOT CLICKED")
                time.sleep(.10)    
    





