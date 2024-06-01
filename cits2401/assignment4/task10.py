""" task10 """

import matplotlib.pyplot as plt
from task5 import generate_4d_data


def star_formation_visualisation(data4d, time_array):
    ################################################################
    #preset, don't touch! (but you can change the names if you want)
    fig, axe = plt.subplots(2, 3, sharex=True, sharey=True)
    ax_lims = 1000
    fig.set_size_inches(14, 7)
    gas_col = 'dimgrey'
    old_col = 'red'
    new_col = 'cyan'
    ################################################################

    rows = 2
    cols = 3
    for row in range(rows):
        for col in range(cols):
            axe[row, col].set_xlim(-ax_lims, ax_lims)
            axe[row, col].set_ylim(-ax_lims, ax_lims)
    
    for time in range(len(time_array)):
        gasX = data4d[time][2][:, 0]
        gasY = data4d[time][2][:, 1]
        gasZ = data4d[time][2][:, 2]
        axe[0, time].scatter(gasX, gasY, c=gas_col, s=1, alpha=0.3)
        axe[1, time].scatter(gasX, gasZ, c=gas_col, s=1, alpha=0.3)

        if time > 0:
            oldX = data4d[time][3][:, 0]
            oldY = data4d[time][3][:, 1]
            oldZ = data4d[time][3][:, 2]
            axe[0, time].scatter(oldX, oldY, c=old_col, s=1)
            axe[1, time].scatter(oldX, oldZ, c=old_col, s=1) 
        
        newX = data4d[time][4][:, 0]
        newY = data4d[time][4][:, 1]
        newZ = data4d[time][4][:, 2]
        axe[0, time].scatter(newX, newY, c=new_col, s=1, alpha=0.1)
        axe[1, time].scatter(newX, newZ, c=new_col, s=1, alpha=0.1)
    
    return plt


def main():
    """ tests star_formation_visualisation() """
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file) 
    plt1 = star_formation_visualisation(data4d, time_array) 
    plt1.show()


if __name__ == "__main__":
    main()
