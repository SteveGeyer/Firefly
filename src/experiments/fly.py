"""Basic flying code."""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import command
import pose

class Fly:
    """Basic flying code."""

    def __init__(self, parser):
        """Initialize the flying code."""
        self.pose = pose.Pose()
        self.cmd = None
        self.marker_id = 0
        self.flying = False
        self.armed = False
        self.image_count = 0
        parser.add_argument('-i', '--id',
                            help='marker ID to find',
                            required=False, type=int, default=2)
        parser.add_argument('-t', '--ttyname',
                            help='Serial tty to transmitter.',
                            required=False,
                            default='/dev/ttyACM0')

    def setup(self, args):
        self.cmd = command.Command(args.ttyname)
        self.marker_id = args.id

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
            print('start flying')
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
