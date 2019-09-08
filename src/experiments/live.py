#!/usr/bin/env python3

"""Run pose processing algorithms over a live feed."""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import argparse
import cv2
import pose

def main():
    """Execute the command"""

    parser = argparse.ArgumentParser(description='Save calibration data')
    parser.add_argument('-i', '--id',
                        help='marker ID to find',
                        required=False, type=int, default=2)
    args = parser.parse_args()

    image_count = 0
    cap = cv2.VideoCapture(0)
    p = pose.Pose()
    while True:
        _, frame = cap.read()
        p.solve(frame, args.id)
        results = p.display_results()
        cv2.imshow('frame', results)
        ch = cv2.waitKey(1) & 0xFF
        if ch == ord('c'):
            name = "raw_image_%d.png" % image_count
            if cv2.imwrite(name, frame):
                print("Captured input %s" % name)
            else:
                print("Error writing %s" % name)
            name = "detect_image_%d.png" % image_count
            if cv2.imwrite(name, results):
                print("Captured detection %s" % name)
            else:
                print("Error writing %s" % name)
            image_count += 1
        if ch == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
