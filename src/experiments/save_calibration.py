#!/usr/bin/env python3

"""Save camera calibration data into a NPZ file.

Right now it is just copying the data from the XML file into
'camera_matrix' and 'dist_coeffs' variables and saving. Later it
should be modifie to do something more sophisticated.

"""

import argparse
import numpy as np

def main():
    """Execute the command"""

    # These numbers came from camera calibration.
    camera_matrix = np.matrix([[2.8067599034455509e+02, 0.0, 320.0],
                               [0.0, 2.8067599034455509e+02, 240.0],
                               [0.0, 0.0, 1.0]])
    dist_coeffs = np.matrix([[3.5445310736500790e-01],
                             [-6.7502492317695906e-01],
                             [0.0],
                             [0.0],
                             [2.7701157048659636e-01]])

    parser = argparse.ArgumentParser(description='Save calibration data')
    parser.add_argument('-f', '--basename',
                        help='basename for file (the "npz" extension is added)',
                        required=False, default='calibration')
    args = parser.parse_args()

    filename = args.basename + '.npz'
    np.savez(filename, cameraMatrix=camera_matrix, distCoeffs=dist_coeffs)
    print("Saved to", filename)

if __name__ == "__main__":
    main()
