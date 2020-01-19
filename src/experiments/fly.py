"""Basic flying code."""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import command
import cv2
import pid
import pose

class Fly:
    """Basic flying code."""

    MAX_ALLOWED_MISSES = 10

    def __init__(self, parser):
        """Initialize the flying code."""
        self.pose = pose.Pose()
        self.cmd = None
        self.marker_id = 0
        self.flying = False
        self.armed = False
        self.image_count = 0
        self.height_pid = pid.PID(False)
        self.height_pid.set_set_point(20.0)  # We want to get to height of gate.
        self.height_pid.set_output_limits(-1.0, 1.0)
        self.height_pid.set_initial_output(-1.0)
        self.height_pid.set_tunings(0.02, 0.0, 0.0, True)
        self.missed_data = 0
        parser.add_argument('-i', '--id',
                            help='marker ID to find',
                            required=False, type=int, default=2)
        parser.add_argument('-t', '--ttyname',
                            help='Serial tty to transmitter.',
                            required=False,
                            default='/dev/ttyACM0')

    def now(self):
        return cv2.getTickCount() / cv2.getTickFrequency()

    def setup(self, args):
        self.cmd = command.Command(args.ttyname)
        self.marker_id = args.id

    def process(self, frame):
        """Process new frame, update flight parameters, and return results."""
        found = self.pose.solve(frame, self.marker_id)
        if self.flying:
            if found:
                h = self.pose.height()
                v = 0.0
                if h is not None:
                    v = self.height_pid.compute(self.now(), h)
                self.cmd.command(v, 0.0, 0.0, 0.0)
                self.missed_data = 0
            else:
                self.missed_data += 1
                if self.missed_data > Fly.MAX_ALLOWED_MISSES:
                    print("missed %d, stopping!" % (self.missed_data))
                    self.stop_flying()
                else:
                    print("missing %d" % (self.missed_data))
        return self.pose.display_results()

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
        if not self.armed:
            print("Must be armed first to fly")
        else:
            self.flying = True
            self.missed_data = 0
            self.height_pid.set_set_point(0.0)
            self.height_pid.prep_for_start(self.now(), 0.0)

    def stop_flying(self):
        """Disarm and stop quadcopter"""
        self.flying = False
        self.cmd.disarm()
        self.armed = False

    def command(self, ch, frame):
        """Process flying character commands and return True."""
        if ch == ord('b'):
            print('binding...')
            self.bind()
            print('  done')
            return True
        if ch == ord('a'):
            self.arm()
            print('armed')
            return True
        if ch == ord('d') or ch == ord('s'):
            self.stop_flying()
            print('stop flying')
            return True
        if ch == ord('f'):
            print('start flying...')
            self.start_flying()
            return True
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
            return True
        return False

    def command_help(self):
        """Print command help"""
        print('b    -- bind the quadcopter\n')
        print('a    -- arm the quadcopter for flight')
        print('d, s -- disarm and stop flying\n')
        print('f    -- fly!\n')
        print('c    -- capture images\n')
