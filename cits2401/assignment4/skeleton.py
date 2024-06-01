import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker
from matplotlib import colors, rcParams
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from matplotlib.colorbar import Colorbar

# RC params
# Don't touch!
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 14
rcParams["axes.edgecolor"] = 'black'
rcParams["legend.edgecolor"] = '0.8'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'
plt.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]

# Simulation units
SIMTIME = 4.7e7     # yr   - time (this is 4.7 * 10^7
MASS = 1e8          # Msun - mass (this is 1 * 10^8
VELOCITY = 20.74    # km/s - velocity
SCALE = 1000        # scaling value

######    ALL ITEMS ABOVE ARE PRE-LOADED IN QUIZZES   ######


### PART 1: DATA handling ###
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



### PART 2: DATA manipulation (pandas) ###
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


### PART 3: Visualisation ###
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


def plot_single_for_multiple(data, color, alpha_num):
    """ returns a scatter plot of particle in data4d at time_step """

    x_data = data[:, 0]
    y_data = data[:, 1]
    plt.scatter(x_data, y_data, c=color, s=1, alpha=alpha_num)


def plot_multiple_particle_xy(data4d, time_step, particles, colors, alphas):
    """ plots multiple particles on a scatterplot and returns the plot """

    data_time_step = data4d[time_step]

    for particle, color, alpha in zip(particles, colors, alphas):
        if particle < 0 or particle > 4:
            print("invalid particle id")
            return None
        plot_single_for_multiple(data_time_step[particle], color, alpha)
    
    return plt
        
        
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


def fmt(x, pos):
    if x == 0:
        return '0'
    a, b = '{:.1e}'.format(x).split('e')
    b = int(b)
    return '${} \times 10^{{{}}}$'.format(a, b)    


def individual_particles(data4d, particles):
    """Plot density of particles"""
    #Already implemented for you
    rang = 500
    my_range = [-500, 500]
    old, new, gas, gal = particles
     
    old_hist, xedges, yedges = np.histogram2d(old.x_scale, 
                                              old.y_scale, 
                                              bins=rang*2, 
                                              range=(my_range, my_range), 
                                              weights=old.mass)
    new_hist, xedges, yedges = np.histogram2d(new.x_scale, 
                                              new.y_scale, 
                                              bins=rang*2, 
                                              range=(my_range, my_range), 
                                              weights=new.mass)
    gas_hist, xedges, yedges = np.histogram2d(gas.x_scale, 
                                              gas.y_scale, 
                                              bins=rang*2, 
                                              range=(my_range, my_range), 
                                              weights=gas.mass)
    gal_hist, xedges, yedges = np.histogram2d(gal.x_scale, 
                                              gal.y_scale, 
                                              bins=rang*2, 
                                              range=(my_range, my_range), 
                                              weights=gal.mass)
    
    
    smoothing_sigma = 15 # Used in gaussian smoothing - larger number more smooth
    
    # not that necessary - just makes the plots look nice
    old_hist = gaussian_filter(old_hist, sigma=smoothing_sigma)
    new_hist = gaussian_filter(new_hist, sigma=smoothing_sigma)
    gas_hist = gaussian_filter(gas_hist, sigma=smoothing_sigma)
    gal_hist = gaussian_filter(gal_hist, sigma=smoothing_sigma)
    
    
    # locations of the text box
    text_x = -420
    text_y = 380
    
    # properties of the textbox
    props = dict(facecolor='white', alpha=0.9)  
    
    # Using gridspec here but this can also be done with subplots as well
    fig = plt.figure()
    grid = gridspec.GridSpec(1, 5, width_ratios=[1, 1, 1, 1, 0.05])  
    cbax = plt.subplot(grid[:, -1])
    ax0 = plt.subplot(grid[0, 0]) # bottom left
    ax1 = plt.subplot(grid[0, 1], sharey=ax0) # bottom right
    ax2 = plt.subplot(grid[0, 2], sharex=ax0) # top left
    ax3 = plt.subplot(grid[0, 3], sharex=ax1, sharey=ax2) # top right
    fig.set_size_inches(16, 3.75)
    
    plt.setp(ax1.get_yticklabels(), visible=False) # more gridspec syntax
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax3.get_yticklabels(), visible=False)
    
    
    gamma = 0.2 # Used in the colorbar normalisation
    cmap = plt.cm.get_cmap('plasma')
    
    # Need to find the maximum mass across all histograms
    gal_max = np.max(gal_hist)
    gas_max = np.max(gas_hist)
    new_max = np.max(new_hist)
    old_max = np.max(old_hist)
    
    # Set this to be the max value of the histograms
    all_max = max([gal_max, gas_max, new_max, old_max])
    
    
    # Start plotting!
    fields = [(ax0, gal_hist, 'Disc Stars'),
              (ax1, gas_hist, 'Gas'),
              (ax2, old_hist, 'Old Stars'),
              (ax3, new_hist, 'New Stars')
              ]
    
    for ax, hist, name in fields:
        im = ax.imshow(hist.T, cmap=cmap, origin='lower', 
                       vmin=0, vmax=all_max, 
                       norm=mcolors.PowerNorm(gamma), 
                       extent=[-rang, rang, -rang, rang])
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.text(text_x, text_y, name, bbox=props)        
        ax.tick_params(direction='in', axis='both', which='both', 
                       bottom=True, top=True, left=True, right=True)

    # Unneccecary astro convention to have all your ticks facing inwards
    grid.update(left=0.05, right=0.95, bottom=0.08, top=0.93, 
              wspace=0.1, hspace=0.05)   
    
    # X Y text locations
    fig.text(0.001, 0.5, 'Y (pc)', va='center', rotation='vertical')
    fig.text(0.5, -0.01, 'X (pc)', va='center')
    
    # Colourbar - use external function to turn it into 
    # scientific notation but not essential
    cb = Colorbar(ax=cbax, mappable=im , format=ticker.FuncFormatter(fmt), 
                  ticks=[1e2, 5e2, 1e3])
    cb.set_label('M$_\odot$pc$^{-2}$', labelpad=10)
    
    plt.show()
    return plt


def compute_center(particles, center):
    changed = []
    for frame in particles:
        frame = frame.assign(x_scale=frame['x']-center[0])
        frame = frame.assign(y_scale=frame['y']-center[1])
        frame = frame.assign(z_scale=frame['z']-center[2])
        changed.append(frame)
    return tuple(changed)

   
def main(): 
    """ Main function executing the whole code.
        Uncomment functions as you go.
    """
    data_file = "low_res_1.dat"       
    
    ##part 1: after completing task 1 functions, below should work correctly.
    data4d, time_array = generate_4d_data(data_file)
    ##convert it to numpy array
    data4d = np.array(data4d)



    ##part 2: after completing task 2 functions, below should work correctly.
    col_header = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'iwas', 'id', 'mass']
    old, new, gas, gal = convert_to_pd(col_header, data4d)
    
    
    
    
    ##part 3: after completing task 3 functions, below should work correctly.
    plot_single_particle_xy(data4d, 0, 2, 'blue')
    gas_col = 'dimgrey'
    old_col = 'cyan' 
    new_col = 'red'
    colors = [gas_col, old_col, new_col]
    alphas = [0.3, 0.1, 1]
    plot_multiple_particle_xy(data4d, 2, [2, 3, 4], colors, alphas)
    
    
    star_formation_visualisation(data4d, time_array) 
    
    ##This is for the last question
    ## X Y Z positions of the 1st old star paricle  
    center = data4d[-1][3][0, 0:3] 
    
    particles = (old, new, gas, gal)
    particles = compute_center(particles, center)
    individual_particles(data4d, particles)

if __name__ == "__main__":
    main()
