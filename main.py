from opencv_camera import ChessboardFinder, ApriltagTargetFinder, StereoCamera, StereoCalibration, Camera, CameraCalibration, findFundamentalMat, UnDistort, visualizeDistortion, visualizeTargetDetections, ApriltagMarker, computeReprojectionErrors, visualizeReprojErrors, drawHorizontalLines, drawEpipolarLines, mosaic, coverage, stereoOverlay, ThreadedCamera, SaveVideo, Compressor

import opencv_camera
import os
from pathlib import Path
import cv2
#import re
import keyboard


def convertImageToGray(image):
    try:
        image = cv2.imread(image)
    except:
        pass
    image = opencv_camera.bgr2gray(image)
    #image = cv2.equalizeHist(image)
    return image

def addToList(image, List):
    List.append(image)
    return List

def removeFromList(index, List):
    del List[index]
    return List

def replaceImageInList(index, List, image):
    List[index] = image
    return List

def iterateFolder(directory):
    for index, filename in enumerate(os.listdir(directory)):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            #newFileName = os.rename("./imgs/"+filename, "./imgs/" + str(index) + ".jpg")
            addToList(directory+filename, imageList)
        if filename.endswith(".png"): 
            addToList(directory+filename, calibrationList)

def printList(List):
    for i in List:
        print(i)              

def takePicture(capture):
    ret, frame = capture.read()
    frame =convertImageToGray(frame)
    return frame
    

def displayImage(windowName, image):
    cv2.imshow(windowName, image)
    
def faceFinder(image, scaleFactor, minFaces, flags, minSize):
    facesFound = tracker.detectMultiScale(image, scaleFactor, minFaces, flags, minSize)
    return facesFound

def faceTracker(facesFound, frame):
    
    for(x,y,w,h) in facesFound:
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        displayImage("Tracking", frame)
        
    return frame

# --------------------------------------------------     
#                        MAIN
# --------------------------------------------------

imageList = list()
calibrationList = list()
#Iterates through the folder and adds the images to the list
iterateFolder("imgs/")
printList(imageList)
printList(calibrationList)

# Iterates throught folder and makes images grey 

for image in imageList:
    newGrayImage = convertImageToGray(image)
    #removeFromList(imageList, imageList.index(image))
    #addToList(newGrayImage, imageList)
    replaceImageInList(imageList.index(image), imageList, newGrayImage)
    
windowName='Grayscale Conversion OpenCV'
# cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
# loop = True
# try:
#     while loop:
#         for image in imageList:
#             displayImage(windowName, image)
#             cv2.waitKey(60)
#             if keyboard.is_pressed('q'):
#                 cv2.destroyAllWindows()
#                 loop = False
#                 break
# except KeyboardInterrupt:
#     cv2.destroyAllWindows()
#     pass

cam = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 

# while(True):
#     cv2.imshow('Live Video',takePicture(cam)) #display the captured image
#     if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
#         cv2.imwrite('imgs/CapturedFrame.png',takePicture(cam))
#         cv2.destroyAllWindows()
#         break
#     elif keyboard.is_pressed('q'):
#         cv2.destroyAllWindows()
#         break

# calibrator = CameraCalibration()
# cap, cal = calibrator.calibrate(imageList, calibrationList[0], )

tracker = cv2.CascadeClassifier('haarcascade_frontalface.xml')

while(True):
    frame = takePicture(cam)
    #frame = cv2.resize(frame, (1080, 1080))
    facesFound = faceFinder(frame, 1.2, 20, cv2.CASCADE_SCALE_IMAGE, (10,10))

    try:
        if facesFound.any() != False:
            faceTracker(facesFound, frame)
    except:
        displayImage("Tracking", frame)
        pass
    if cv2.waitKey(1) & 0xFF == ord('y'):
        cv2.imwrite('imgs/CapturedFrame.png',takePicture(cam))
        cv2.destroyAllWindows()
        break
    elif keyboard.is_pressed('q'):
        cv2.destroyAllWindows()
        break
