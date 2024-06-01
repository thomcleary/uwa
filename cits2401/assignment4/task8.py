""" task 8 """

import matplotlib.pyplot as plt
from task5 import generate_4d_data


def plot_single_particle_xy(data4d, time_step, particle, color):
    """ returns a scatter plot of particle in data4d at time_step """
    if particle < 0 or particle > 4:
        print("invalid particle id")
        return None

    particle_data = data4d[time_step][particle]
    x_data = particle_data[:, 0]
    y_data = particle_data[:, 1]
    plt.scatter(x_data, y_data, c=color, s=1, alpha=0.3)
    return plt



def main():
    """ tests plot_single_particle_xy() """

    print("Test 1")
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    time_step = 0
    particle = 2
    plt1 = plot_single_particle_xy(data4d, time_step, particle, 'blue')
    plt1.show()
    print()

    print("Test 2")
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    time_step = 0
    particle = 5
    #catches errors
    plot_single_particle_xy(data4d, time_step, particle, 'blue')
    print()



if __name__ == "__main__":
    main()
