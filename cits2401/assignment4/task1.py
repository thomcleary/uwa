""" task1 """

def init_array():
    """ return a tuple of 5 empty lists """
    return ([], [], [], [], [])


def main():
    """ tests init_array """
    test_tuple = init_array()
    print(test_tuple)
    print("Expected Length: 5\nGot {}".format(len(test_tuple)))


main()