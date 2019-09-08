#!/usr/bin/env python3

"""Run pose processing algorithms over a single image and show the image it."""

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
    parser.add_argument('-f', '--filename',
                        help='source image',
                        required=False, default='images/raw_image_0.png')
    args = parser.parse_args()

    p = pose.Pose()
    frame = cv2.imread(args.filename)
    p.solve(frame, args.id)
    cv2.imshow('frame', p.display_results())
    cv2.waitKey(10000)

if __name__ == "__main__":
    main()
