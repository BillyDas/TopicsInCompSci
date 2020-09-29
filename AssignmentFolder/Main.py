from cv2 import *
import numpy as np
import math
import RPi.GPIO as GPIO
import time

# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()

GPIO.setmode(GPIO.BCM)

#RPIE Setup
left_Stopper = 6
Right_Stopper = 5
FullDetection = 0
GPIO.setup(left_Stopper, GPIO.IN)
GPIO.setup(Right_Stopper, GPIO.IN)

left = 1
right = 0

personLeft = []
personRight = []

#MATH SETUP
PLX = 0

x_origin = None
y_origin = None

x_adjacent = None
y_adjacent = None
#Camera Setup

pixel_width = 1280
pixel_height = 720

angle_width = 52
angle_height = 23
camera_separation = 335



global person

#Final Math Formula is
#Length = D / Tan(LeftCord) + D / Tan(RightCord)

#def left_cam_distance():
    #formula is TAN = Opposit / Adjuacent
    # which will be D

def readinput():
    global LSwitchIsOn
    global RSwitchIsOn
    LSwitchIsOn = GPIO.input(left_Stopper)
    RSwitchIsOn = GPIO.input(Right_Stopper)


def take_photo_process_photo(left_cam_true):
    # Setup Detection Enviroment
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    IGNORE = set(["person"])
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


    #Take Picture
    print("[CAMERA] - Taking Picture One")
    imgsaveloc = "/home/pi/Desktop/AssignmentFolder/"
    #imgfilename = "LeftImg.png"
    imgfilename = "LeftPos.jpg"

    #imwrite(imgfilename,img) #save image
    print("[CAMERA] - Picture Taken")
    # Loads First Image Taken
    image = cv2.imread(imgfilename)

    #loads serialised model (basically loads the network as a model)
    model = "/home/pi/Desktop/AssignmentFolder/MobileNetSSD_deploy.caffemodel"
    prototxt = "/home/pi/Desktop/AssignmentFolder/MobileNetSSD_deploy.prototxt.txt"
    net = cv2.dnn.readNetFromCaffe(prototxt,model)

    # Checks the Rows Columns of the image, then normilises it to 300x300
    (h, w) = image.shape[:2]
    # Sets The Image Resolution to 300x300 (this creates a
    # cv2.resize args (Soruce, SizeWanted, Scale factor for X axis, Scale Factor For Y axis)
    imageModified = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # Adds the image to the "network" meaning the AI Network


    # Adds Crosshair to the TEST IMAGE (FOR ALLIGNMENT)

    allignmentimage = cv2.resize(image, (300, 300))
    x_origin = int(pixel_width/2)
    y_origin = int(pixel_height/2)

    #Adds a croshair to the image (used to allign the camera)
    #cv2.line(allignmentimage,(0,y_origin),(pixel_width,y_origin),(0,255,0),1)
    #cv2.line(allignmentimage,(x_origin,0),(x_origin,pixel_height),(0,255,0),1)
    #cv2.circle(allignmentimage,(x_origin,y_origin),int(round(y_origin/8,0)),(0,255,0),1)

    imwrite("lineup.jpg",allignmentimage)
    net.setInput(imageModified)
    detections = net.forward()


    print("[NETWORK] - New Network Item Added (LeftCamSnap)")

    print("[NETWORK] - Beggining Network Item Processing.")
    # Create an empty array for player cords

    # loop over the detections (LIST OF DETECTION VALUES]

    for i in np.arange(0, detections.shape[2]):
        # extract the confidence associated with the prediction
        # [INFO] confidence is how sure the network is of an object.
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is great that 80%
        if confidence > 0.2:

            idx = int(detections[0, 0, i, 1])

            if CLASSES[idx] in IGNORE:


                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # display the prediction
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.rectangle(image, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                # calculates the center point of the person by taking the
                # boundaries of the rectagle it draws
                # around the person, and finds the center of that.
                centerperson = (int((startX+endX)/2),int((startY+endY)/2))
#                print("[INFO] : Center Cords of Person : ", centerperson)
                if left_cam_true == True:
                    personLeft.append(centerperson)
                elif left_cam_true != True:
                    personRight.append(centerperson)


                # draws the circle around the center point
                cv2.circle(image,centerperson, 4, (255,0,255), 4)


                # Displays the image (for debugging
                #cv2.imshow("Output", image)

    print("Listing Person Cordinates (Pixels)")
    if left_cam_true == True:
        return personLeft
    elif left_cam_true != True:
        return personRight





#-----------------------------------------------
#-                    MATH TIME!               -
#-----------------------------------------------

def math_time(personLeft, personRight):

    #Calculates Angles of the left and right camera (full angles add up to 180)
    B1 = (180-angle_width)/2
    B2 = (180-angle_width)/2
    print("B1:" B1)
    print("B2:" B2)
    #grabs the X aix pixel cordinate.

    for i in person:
        PLX = personLeft[i].split(", ")[0]
        PRX = personRight[i].split(", ")[0]


        #Gets the distance of the X cordinates from the 0,0 position (top left)
        AP1 = angle_width / PLX
        AP2 = angle_width / PRX

        P1 = pixel_width - PLX
        P2 = PRX - 1

        O1 = P1 * AP1
        O2 = P2 * AP2

        Theta = P1 * (angle_width / pixel_width) + B1
        Phi = P2 * (angle_width / pixel_width) + B2

        Car_angle = 180 - (Phi - Theta)

        Distance = (camera_separation * math.sin(math.radians(Phi) * math.sin(math.radians(Theta))))/math.sin(math.radians(180 - (Theta + Phi)))

#if not angle_height:
#
#angle_height = angle_width*(pixel_height/pixel_width)
#            print(angle_height)
#

#args = {'image': 'images/LeftCamSnap.jpg', 'model': 'MobileNetSSD_deploy.caffemodel', 'prototxt': 'MobileNetSSD_deploy.prototxt.txt', 'confidence': 0.2}



#----------------------------MAIN FUNCTION CALLER-------------------------------
print("[INFO] - Program ")


while 1:
    if left == 1:
        while left == 1:
            #------Left Stopper
            readinput()
            #if LSwitchIsOn == 1:
            if LSwitchIsOn == 0:
                #Activate Webcam Photo
                print("we here")
                take_photo_process_photo(left_cam_true=True)
                for t in personLeft:
                    print(t)

                print("RED CLICKED")
                time.sleep(.10)
                left = 0
                right = 1
                FullDetection = FullDetection + 1
            elif LSwitchIsOn == 0:
                print("RED NOT CLICKED")
                time.sleep(.10)

    elif right == 1:
        while right == 1:
            #------Right Stopper
            readinput()
            if RSwitchIsOn == 1:
                #Activate Webcam Photo
                print("we here")
                take_photo_process_photo(left_cam_true=False)
                for t in personRight:
                    print(t)

                print("GREEN CLICKED")
                time.sleep(.10)
                left = 1
                right = 0
                FullDetection = FullDetection + 1
            elif RSwitchIsOn == 0:
                print("GREEN NOT CLICKED")
                time.sleep(.10)
    elif FullDetection == 2:
        math_time(personLeft,personRight)
        personLeft = []
        personRight = []
        print("Full Detection Done")
