""" task2 """

import numpy as np

def convert_to_np(components):
    """ returns new list with elements in components converted to numpy
        arrays
    """
    numpy_components = []

    for element in components:
        numpy_components.append(np.array(element))

    return numpy_components


def main():
    """ tests convert_to_np() """
    components = [[1, 2], [3, 4], [5, 6]]

    np_components = convert_to_np(components)

    print(np_components)


if __name__ == "__main__":
    main()