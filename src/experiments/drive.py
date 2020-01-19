#!/usr/bin/env python3

"""Drive the quadcopter from a command line for testing.

b -- bind the quadcopter

a -- arm the quadcopter for flight
d -- disarm and stop flying

A line of one to four numbers in the range of 0.0 to 1.0 separated by
spaces. They are in the order of throttle, direction, forward/backwards,
and rotation. Missing numbers will be filled in with the value 0.5.

q -- quit program
"""

__author__ = "Steve Geyer"
__copyright__ = "Copyright 2019, Steve Geyer"
__credits__ = ["Steve Geyer"]
__license__ = "BSD 3-Clause License"
__version__ = "1.0.0"
__status__ = "Development"

import argparse
import command

def help():
    print('b    -- bind the quadcopter\n')
    print('a    -- arm the quadcopter for flight')
    print('d    -- disarm and stop flying\n')
    print('A line of one to four numbers in the range of 0.0 to 1.0 separated\n'
          +'by spaces. They are in the order of throttle, direction,\n'
          +'forward/backwards, and rotation. Missing numbers will be filled\n'
          + 'in with the value 0.5.\n')
    print('q    -- quit program')
    print('h, ? -- this help')


def execute(c, text):
    """Grab values and command quad."""
    parts = text.split()
    if not parts:
        print("Must have at least one number")
        return

    try:
        throttle = float(parts[0])
        if len(parts) > 1:
            direction = float(parts[1])
        else:
            direction = 0.5
        if len(parts) > 2:
            forward = float(parts[2])
        else:
            forward = 0.5
        if len(parts) > 3:
            rotation = float(parts[3])
        else:
            rotation = 0.5
        print(('throttle:%.2f direction:%.2f '
               +'forward:%.2f rotation:%.2f') % (throttle, direction,
                                                 forward, rotation))
        c.command(throttle, direction, forward, rotation)
    except ValueError:
        print('Bad number')

def main():
    """Execute the command"""

    parser = argparse.ArgumentParser(description='Drive quadcopter from a command line')
    parser.add_argument('-t', '--ttyname',
                        help='Serial tty to transmitter.',
                        required=False,
                        default='/dev/ttyACM0')
    args = parser.parse_args()

    c = command.Command(args.ttyname)
    while True:
        text = input('> ')
        if text == 'a':
            c.arm()
            print('Armed')
        elif text == 'b':
            print('Binding...')
            c.bind()
            print('  done')
        elif text == 'd':
            c.disarm()
            print('Disarm')
        elif text == '':
            continue
        elif text == 'q':
            break
        elif text == 'h':
            help();
        elif text == '?':
            help();
        else:
            execute(c, text)

if __name__ == "__main__":
    main()
