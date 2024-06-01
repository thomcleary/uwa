""" task3 """

import numpy as np

# Simulation units
SIMTIME = 4.7e7     # yr   - time (this is 4.7 * 10^7
MASS = 1e8          # Msun - mass (this is 1 * 10^8
VELOCITY = 20.74    # km/s - velocity
SCALE = 1000        # scaling value


def scale_arrays(array):
    """ returns scaled array """
    if array.size == 0:
        return array

    array_copy = np.copy(array)
    array_copy[:, 0:3] *= SCALE
    array_copy[:, 3:6] *= VELOCITY
    array_copy[:, 6]    = array_copy[:, 6].astype(int)
    array_copy[:, 8]   *= MASS

    return array_copy


def main():
    """ tests scale_arrays() """
    array = np.array([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]])
    got = scale_arrays(array)
    print(got)
    print()

    array = np.array([[-1.78, -1.81,  8.07,  1.07, -3.64, 5.73,  0.0,  1.0,  1.67],
                  [-4.54, -9.43,  9.38,  7.96,  1.26, 7.48,  0.0,  2.0,  1.67]])
    got = scale_arrays(array)
    print(got)
    print()

    array = np.array([[]])
    got = scale_arrays(array)
    print(got)
    print()

    
if __name__ == "__main__":
    main()
