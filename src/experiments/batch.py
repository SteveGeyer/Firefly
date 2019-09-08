#!/usr/bin/env python3

"""Run pose processing algorithms over a series of images."""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import argparse
import os
import cv2
import pose

def main():
    """Execute the command"""
    parser = argparse.ArgumentParser(description='Save calibration data')
    parser.add_argument('-i', '--id',
                        help='marker ID to find',
                        required=False, type=int, default=2)
    parser.add_argument('-r', '--results',
                        help='result directory',
                        required=False, default='results')
    parser.add_argument('-s', '--source',
                        help='source directory for images',
                        required=False, default='images')
    args = parser.parse_args()

    # Make sure output directory exists before we start.
    try:
        os.mkdir(args.results)
    except FileExistsError:
        pass

    # Process files.
    p = pose.Pose()
    for name in os.listdir(args.source):
        frame = cv2.imread(args.source + '/' + name)
        p.solve(frame, args.id)
        cv2.imwrite(args.results + '/' + name, p.display_results())

if __name__ == "__main__":
    main()
