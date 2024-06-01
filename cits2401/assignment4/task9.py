""" task9 """

import matplotlib.pyplot as plt
from task5 import generate_4d_data


# task 9 helper
def plot_single_for_multiple(data, color, alpha_num):
    """ returns a scatter plot of particle in data4d at time_step """

    x_data = data[:, 0]
    y_data = data[:, 1]
    plt.scatter(x_data, y_data, c=color, s=1, alpha=alpha_num)


# task 9
def plot_multiple_particle_xy(data4d, time_step, particles, colors, alphas):
    """ plots multiple particles on a scatterplot and returns the plot """

    data_time_step = data4d[time_step]

    for particle, color, alpha in zip(particles, colors, alphas):
        if particle < 0 or particle > 4:
            print("invalid particle id")
            return None
        plot_single_for_multiple(data_time_step[particle], color, alpha)

    return plt
        

def main():
    """ tests plot_multiple_particle_xy() """
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    gas_col = 'dimgrey'
    old_col = 'red' 
    new_col = 'cyan'
    colors = [gas_col, old_col, new_col]
    alphas = [0.3, 1, 0.1]
    plt1 = plot_multiple_particle_xy(data4d, 2, [2, 3, 4], colors, alphas)
    plt1.show()

    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    gas_col = 'dimgrey'
    old_col = 'red' 
    new_col = 'cyan'
    colors = [gas_col, old_col, new_col]
    alphas = [0.3, 1, 0.1]
    #check error
    plot_multiple_particle_xy(data4d, 2, [2, 3, 5], colors, alphas)


if __name__ == "__main__":
    main()
