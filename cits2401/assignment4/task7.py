""" task7 """

import pandas as pd
from task5 import generate_4d_data
from task6 import convert_to_pd


def particle_stats(particle, col_name):
    """ returns min, average and max values of col_name in particle """
    columns = list(particle.columns.values)
    
    if col_name not in columns:
        return None
    
    column = particle[col_name]

    values = []
    values.append(column.min())
    values.append((column.sum()) / len(column))
    values.append(column.max())

    return values

    
def main():
    """ tests particles_stats() """

    print("Test 1")
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    col_header = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'iwas', 'id', 'mass']
    old, new, gas, gal = convert_to_pd(col_header, data4d)
    vals = [round(val, 2) for val in particle_stats(old, 'x')]
    print(vals)
    print()

    print("Test 2")
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    col_header = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'iwas', 'id', 'mass']
    old, new, gas, gal = convert_to_pd(col_header, data4d)
    print(particle_stats(new, 'xx'))
    print()


if __name__ == "__main__":
    main()