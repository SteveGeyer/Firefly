"""Determine quadcopter's pose using a pair of Aruco fiducial makers."""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import math
import numpy as np
import cv2
from cv2 import aruco

class Pose:
    """Determine quadcopter's pose using a pair of Aruco fiducial makers."""

    # Set up aruco markers as class variables.
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    aruco_params = aruco.DetectorParameters_create()

    # Aruco target parameters.
    target_size = 12.3     # Aruco target size in cm.
    target_dist = 32.2     # Distance between center of targets in cm.

    # 'target_objp' defined the points around the two markers. We
    # start at the upper left hand point of the left hand marker and
    # go clockwise. Then we do the upper left hand point of the right
    # marker and go clockwise. Everthing is positioned relative to the
    # center of the gate we want to transition through.
    max_dx = (target_size + target_dist)/2
    min_dx = max_dx - target_size
    dy = target_size/2
    target_objp = np.array([[-max_dx, -dy, 0],
                            [-min_dx, -dy, 0],
                            [-min_dx, dy, 0],
                            [-max_dx, dy, 0],
                            [min_dx, -dy, 0],
                            [max_dx, -dy, 0],
                            [max_dx, dy, 0],
                            [min_dx, dy, 0]], np.float32)

    # Set up camera calibration data as class variables.
    with np.load('calibration.npz') as x:
        camera_matrix = x['cameraMatrix']
        dist_coeffs = x['distCoeffs']


    def __init__(self):
        """Initialize pose with image"""
        self.frame = None       # Input image frame.
        self.gray = None        # Undisorted gray scale image to process.
        self.corners = None     # Corners of detected fiducial markers.
        self.ids = None         # IDs of detected fiducial markers.
        self.rvecs = None       # Rotation vector of detected markers.
        self.tvecs = None       # Translation vector of detected markers.
        self.found = False      # True if detected and processed both markers.
        self.runtime = 0        # Runtime of last solve.
        self.status = None      # Status information.

    def solve(self, frame, expected_id):
        """Solve for quadcopter pose"""
        e1 = cv2.getTickCount()
        self.frame = frame
        self.gray = create_gray_frame(frame)
        self.corners, self.ids = detect_markers(self.gray, expected_id)
        if self.corners is not None and len(self.corners) == 2:
            self.found, self.rvecs, self.tvecs = position_markers(self.corners)
        else:
            self.found = False
            self.rvecs = None
            self.tvecs = None
        self.runtime = (cv2.getTickCount() - e1)/cv2.getTickFrequency()*1000
        return self.found


    def display_results(self):
        """Create image and display results on it"""
        result = cv2.cvtColor(self.gray, cv2.COLOR_GRAY2BGR)
        if self.corners is None:
            return result

        # Draw the fiduals found.
        result = aruco.drawDetectedMarkers(result, self.corners, self.ids)

        if self.found:
            seglen = 8
            axis = np.float32([
                [0, 0, 0],       # Center point
                [seglen, 0, 0],  # X axis
                [0, seglen, 0],  # Y axis
                [0, 0, -seglen]  # Z axis
            ]).reshape(-1, 3)
            imgpts, _ = cv2.projectPoints(axis, self.rvecs, self.tvecs,
                                          Pose.camera_matrix, Pose.dist_coeffs)
            result = draw_axis(result, imgpts)
            self.add_status(result)
        return result


    def add_status(self, result):
        """Display status information on the result image"""
        rad2deg = 180/math.pi
        color = (200, 255, 255)
        if self.found:
            color = (0, 255, 255)
            self.status = (self.tvecs[0][0],
                           self.tvecs[1][0],
                           self.tvecs[2][0],
                           self.rvecs[0][0]*rad2deg,
                           self.rvecs[1][0]*rad2deg,
                           self.rvecs[2][0]*rad2deg,
                           segment_length(self.tvecs[0][0],
                                          self.tvecs[1][0],
                                          self.tvecs[2][0]))
        s = self.status
        msg = ("%.1f ms (%.1f, %.1f, %.1f) "+
               "r:(%.1f, %.1f, %.1f) len:%.1f") % (self.runtime,
                                                   s[0], s[1], s[2],
                                                   s[3], s[4], s[5], s[6])
        cv2.putText(result, msg, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    color, lineType=cv2.LINE_AA)


def create_gray_frame(frame):
    """Create and return an undistorted grayscale image"""
    h, w = frame.shape[:2]
    new_matrix, _ = cv2.getOptimalNewCameraMatrix(Pose.camera_matrix,
                                                  Pose.dist_coeffs,
                                                  (w, h), 1, (w, h))
    fixed = cv2.undistort(frame, Pose.camera_matrix, Pose.dist_coeffs,
                          None, new_matrix)
    return cv2.cvtColor(fixed, cv2.COLOR_BGR2GRAY)


def detect_markers(gray, expected_id):
    """Detect and return corners with the correct ID."""
    d_corners, d_ids, _ = aruco.detectMarkers(gray,
                                              Pose.aruco_dict,
                                              parameters=Pose.aruco_params,
                                              cameraMatrix=Pose.camera_matrix)

    # Only keep the corners from the expected IDs.
    ids = np.array([])
    corners = []
    for i in range(len(d_corners)):
        if d_ids[i][0] == expected_id:
            np.append(ids, d_ids[i])
            corners.append(d_corners[i])

    return corners, ids


def draw_axis(img, imgpts):
    """Draw an x, y, z axis on image."""
    corner = tuple(imgpts[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (255, 0, 0), 3)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 255, 0), 3)
    img = cv2.line(img, corner, tuple(imgpts[3].ravel()), (0, 0, 255), 3)
    return img


def segment_length(x, y, z):
    """Return the length of the segment."""
    return math.sqrt(x*x+y*y+z*z)


def position_markers(corners):
    """Take 2D points and apply against 3D model of fiducial markers."""
    p1 = np.array(corners[0][0], np.float32)
    p2 = np.array(corners[1][0], np.float32)
    if p1[0][0] > p2[0][0]:
        p1, p2 = p2, p1
    all_corners = np.concatenate((p1, p2), axis=0)
    return cv2.solvePnP(Pose.target_objp, all_corners,
                        Pose.camera_matrix, Pose.dist_coeffs)
