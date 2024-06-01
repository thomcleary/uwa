""" task6 """

import task5
import pandas as pd



def convert_to_pd(col_header, data4d):
    """ returns pandas data frame objects in a tuple.
        (old, new, gas, gal)
    """
    # last time-step
    # disc-stars, gas, old-stars, new-stars
    last_particles = data4d[-1][1:]
    frames = []

    for particle in last_particles:
        data_frame = pd.DataFrame(particle[:, 0:9])
        data_frame.columns = col_header
        frames.append(data_frame)

    frames = tuple([frames[2], frames[3], frames[1], frames[0]])
    return frames


def main():
    """ tests convert_to_pd """

    print('Test 1')
    data_file = "low_res_1.dat"
    data4d, time_array = task5.generate_4d_data(data_file)
    col_header = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'iwas', 'id', 'mass']      
    convert_to_pd(col_header, data4d)
    old, new, gas, gal = convert_to_pd(col_header, data4d)
    print(old.head(3))
    print()

    print("Test 2")
    data_file = "low_res_1.dat"
    data4d, time_array = task5.generate_4d_data(data_file)
    col_header = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'iwas', 'id', 'mass']
    old, new, gas, gal = convert_to_pd(col_header, data4d)
    print(new.head(3))
    print()

if __name__ == "__main__":
    main()
