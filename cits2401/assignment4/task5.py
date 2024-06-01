""" task 5 """

import numpy as np

# Simulation units
SIMTIME = 4.7e7     # yr   - time (this is 4.7 * 10^7
MASS = 1e8          # Msun - mass (this is 1 * 10^8
VELOCITY = 20.74    # km/s - velocity
SCALE = 1000        # scaling value


def init_array():
    """ return a tuple of 5 empty lists """
    return ([], [], [], [], [])


def convert_to_np(components):
    """ returns new list with elements in components converted to numpy
        arrays
    """
    numpy_components = []

    for element in components:
        numpy_components.append(np.array(element))

    return numpy_components


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


def generate_timestamp(components):
    """ converts 3d list to numpy arrays in list and scales their values """
    components = convert_to_np(components)

    for index, elements in enumerate(components):
        components[index] = scale_arrays(elements)

    return components


def generate_4d_data(data_file):
    particles = list(init_array())
    time_steps = []
    data_4d = []

    with open(data_file, 'r') as in_file:
        for line in in_file:

            line = line.strip().split()
            length = len(line)

            line = np.fromstring(" ".join(line), count=length, sep=" ")

            if length == 2:
                time_steps.append(line[1] * SIMTIME)
                if len(time_steps) > 1:
                    data_4d.append(generate_timestamp(particles))
                    particles = list(init_array())

            elif length == 12:
                iD = int(line[6])
                if iD < 0 or iD > 4:
                    print("WARNING: unknown ID argument")
                    return None
                particles[iD].append(line)

    data_4d.append(generate_timestamp(particles))
    return (data_4d, time_steps)


def main():
    """ tests init_array() """
    data_4d, time_steps = generate_4d_data("low_res_1.dat")

    print(data_4d[1][2][3])
    print()
    print(time_steps)

if __name__ == "__main__":
    main()
