#!/usr/bin/env python3

"""Show the drone camera on the screen.

You can use this to verify that that data path from the drone, through
the FPV Video Receiver and all the way into the NVIDIA Nano works. It
also verifies that Python and OpenCV are set up correctly.

"""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import argparse
import cv2

def interactive_help():
    """Print interactive help"""
    print('q    -- quit program')
    print('h, ? -- this help')

def process_command():
    """Get character and process command. Return True to stop running."""
    ch = cv2.waitKey(1) & 0xFF
    if ch == ord('h') or ch == ord('?'):
        interactive_help()
    elif ch == ord('q'):
        return False
    return True

def main():
    """Execute the command"""
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        cv2.imshow('frame', frame)
        if not process_command():
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
