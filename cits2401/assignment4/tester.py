from final import *

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
    old_col = 'red' 
    new_col = 'cyan'
    colors = [gas_col, old_col, new_col]
    alphas = [0.3, 1, 0.1]
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
