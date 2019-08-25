#!/usr/bin/env python3

# Perform experiments in analysis of the sample images.

import os
import cv2
from cv2 import aruco

images_directory = 'images'
detects_directory = 'detects'

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
aruco_params =  aruco.DetectorParameters_create()

def processImage(filename):
    "Process an image and perform marker calculations"
    frame = cv2.imread(images_directory + '/' + filename)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray,
                                                 aruco_dict,
                                                 parameters=aruco_params)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    cv2.imwrite(detects_directory + '/' + filename, frame_markers)


# Make sure output directory exists before we start.
try:
    os.mkdir("detects")
except FileExistsError:
    pass

# Process files.
for filename in os.listdir('images'):
    processImage(filename)
