#!/usr/bin/env python3

"""Create an Aruco markers for testing.

It can create a single marker or a pair for easy testing.
"""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
from cv2 import aruco


def main():
    """Execute the command"""

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    fig = plt.figure()

    parser = argparse.ArgumentParser(description='Create aruco fiducial markers')
    parser.add_argument('-b', '--basename',
                        help='basename for file (an extension is added)',
                        required=False, default='marker')
    parser.add_argument('-i', '--id', type=int, help='marker ID',
                        required=False, default=1)
    parser.add_argument('-p', '--pair', help='create a pair of markers',
                        required=False, action='store_true')
    args = parser.parse_args()

    if not args.pair:
        img = aruco.drawMarker(aruco_dict, args.id, 700)
        filename = args.basename + '.png'
        cv2.imwrite(filename, img)
        print('Created ID %d marker into file %s' % (args.id, filename))
    else:
        ax = fig.add_subplot(1, 4, 1)
        img = aruco.drawMarker(aruco_dict, args.id, 700)
        plt.imshow(img, cmap=mpl.cm.gray, interpolation='nearest')
        ax.axis('off')
        ax = fig.add_subplot(1, 4, 4)
        img = aruco.drawMarker(aruco_dict, args.id, 700)
        plt.imshow(img, cmap=mpl.cm.gray, interpolation='nearest')
        ax.axis('off')
        filename = args.basename + '.pdf'
        plt.savefig(filename)
        print('Created pair of ID %d markers into file %s' % (args.id, filename))

if __name__ == "__main__":
    main()
