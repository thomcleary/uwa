""" task4 """
from task2 import convert_to_np
from task3 import scale_arrays

def generate_timestamp(components):
    """ converts 3d list to numpy arrays in list and scales their values """
    components = convert_to_np(components)

    for index, elements in enumerate(components):
        components[index] = scale_arrays(elements)

    return components


def main():
    """ tests generate_timestamp() """
    array = [
        [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]],
        [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]]
    ]
    print(generate_timestamp(array))
    # [
    #   array([[1.0000e+03, 2.0000e+03, 3.0000e+03, 8.2960e+01, 1.0370e+02,
    #         1.2444e+02, 7.0000e+00, 8.0000e+00, 9.0000e+08]
    #   ]),
    #   array([[1.0000e+03, 2.0000e+03, 3.0000e+03, 8.2960e+01, 1.0370e+02,
    #         1.2444e+02, 7.0000e+00, 8.0000e+00, 9.0000e+08]
    #   ])
    # ]


if __name__ == "__main__":
    main()