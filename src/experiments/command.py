"""Drive the transmitter to command the quadcopter."""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import time
import serial

class Command:
    """Drive the transmitter to command the quadcopter."""

    MIN_VALUE = 204
    MAX_VALUE = 1844

    def __init__(self, ttyname):
        """Open serial using ttyname"""
        self.serial = serial.Serial(ttyname)
        self.serial.write(b'\n')
        self.disarm()

    def bind(self):
        """Bind to quadcopter"""
        self.serial.write(b'q')
        time.sleep(1.0)
        self.disarm()

    def arm(self):
        """Arm quadcopter for flight"""
        self.serial.write(b'a')

    def disarm(self):
        """Disarm and stop quadcopter"""
        self.serial.write(b'd')

    def command(self, throttle, direction, forward, rotation):
        """Command each degree of freedom using value 0.0 to 1.0"""
        cmd = b'!%d %d %d %d\n' % (normalize(throttle),
                                   normalize(direction),
                                   normalize(forward),
                                   normalize(rotation))
        self.serial.write(cmd)

def normalize(value):
    """Covert float into integer command value.
       -1.0 => MIN_VALUE through to 1.0 => MAX_VALUE."""
    return min(Command.MAX_VALUE,
               max(Command.MIN_VALUE,
                   ((value+1.0)/2.0)*(Command.MAX_VALUE-Command.MIN_VALUE) +
                   Command.MIN_VALUE))
