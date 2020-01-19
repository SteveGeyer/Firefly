#!/usr/bin/env python3

"""Run pose processing algorithms and drive the drone.

You must have the output window active to process the commands which
are each single letters.

To fly you first must arm the drone using the 'a' command. In about a
second the drone should start spinning it props.

Type 'f' to start flying.

Type 's' to start flying.

Type 'q' to quit the program.

"""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import argparse
import cv2
import fly

def interactive_help(f):
    """Print interactive help"""
    f.command_help()
    print('q    -- quit program')
    print('h, ? -- this help')

def process_command(f, frame):
    """Get character and process command. Return True to stop running."""
    ch = cv2.waitKey(1) & 0xFF
    if f.command(ch, frame):
        return True
    if ch == ord('h') or ch == ord('?'):
        interactive_help(f)
    elif ch == ord('q'):
        return False
    return True

def main():
    """Execute the command"""
    parser = argparse.ArgumentParser(description='Run quadcopter in live mode')
    f = fly.Fly(parser)
    args = parser.parse_args()
    f.setup(args)
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        results = f.process(frame)
        cv2.imshow('frame', results)
        if not process_command(f, frame):
            break
    f.stop_flying()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
