#!/usr/bin/env python3

import argparse
import cv2
import pid

DT = 0.1

class Simulate:
    TIME_CONSTANT = 0.97

    def __init__(self):
        self.out = 0.0

    def update(self, input):
        self.out = self.out*self.TIME_CONSTANT + input*(1.0-self.TIME_CONSTANT)

def main():
    s = Simulate()
    p = pid.PID(True)
    p.set_output_limits(0.0, 10.0)
    p.set_tunings(30.0, 5.0, 5.0, True)
    p.set_set_point(8.0)
    now = 0.0
    p.prep_for_start(now, 0.0)
    for x in range(100):
        now += DT
        startout = s.out
        o = p.compute(now, startout)
        s.update(o)
        msg = "now:%4.1f startval:%6.3f controlOut:%6.3f => %6.3f"
        print(msg % (now, startout, o, s.out))

if __name__ == "__main__":
    main()
