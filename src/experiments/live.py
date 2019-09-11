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
import command

class Fly:
    """Basic flying code."""

    def __init__(self, ttyname, marker_id):
        """Initialize the flying code."""
        self.pose = pose.Pose()
        self.cmd = command.Command(ttyname)
        self.marker_id = marker_id
        self.flying = False
        self.armed = False

    def process(self, frame):
        """Process new frame, update flight parameters, and return results."""
        self.pose.solve(frame, self.marker_id)
        results = self.pose.display_results()
        return results

    def bind(self):
        """Bind to quadcopter"""
        self.cmd.bind()
        self.armed = False

    def arm(self):
        """Arm quadcopter for flight"""
        self.cmd.arm()
        self.armed = True

    def start_flying(self):
        """Start flying the quadcopter"""
        if self.armed:
            self.flying = True
        else:
            print("Must be armed first to fly")

    def stop_flying(self):
        """Disarm and stop quadcopter"""
        self.flying = False
        self.cmd.disarm()
        self.armed = False


def interactive_help():
    """Print interactive help"""
    print('a    -- arm the quadcopter for flight')
    print('d, s -- disarm and stop flying\n')
    print('f    -- fly!\n')
    print('b    -- bind the quadcopter\n')
    print('q    -- quit program')
    print('h, ? -- this help')

def main():
    """Execute the command"""

    parser = argparse.ArgumentParser(description='Save calibration data')
    parser.add_argument('-i', '--id',
                        help='marker ID to find',
                        required=False, type=int, default=2)
    parser.add_argument('-t', '--ttyname',
                        help='Serial tty to transmitter.',
                        required=False,
                        default='/dev/ttyACM0')
    args = parser.parse_args()

    fly = Fly(args.ttyname, args.id)
    image_count = 0
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        results = fly.process(frame)
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
        if ch == ord('b'):
            print('binding...')
            fly.bind()
            print('  done')
        elif ch == ord('a'):
            fly.arm()
            print('armed')
        elif ch == ord('d') or ch == ord('s'):
            fly.stop_flying()
            print('stop flying')
        elif ch == ord('f'):
            print('start flying')
            fly.start_flying()
        elif ch == ord('h') or ch == ord('?'):
            interactive_help()
        elif ch == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
