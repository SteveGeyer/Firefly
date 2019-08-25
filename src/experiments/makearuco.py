#!/usr/bin/env python3

# Create an Aruco markers for testing.

import cv2
from cv2 import aruco
import matplotlib as mpl
import matplotlib.pyplot as plt

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
fig = plt.figure()

marker_id = 1
ax = fig.add_subplot(1, 4, 1)
img = aruco.drawMarker(aruco_dict, marker_id, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")

marker_id = 1
ax = fig.add_subplot(1, 4, 4)
img = aruco.drawMarker(aruco_dict, marker_id, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")

plt.savefig("markers.pdf")
plt.show()
