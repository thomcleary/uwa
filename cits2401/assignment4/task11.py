""" task 11 """

from task5 import generate_4d_data
from task7 import convert_to_pd
from skeleton import individual_particles


def compute_center(particles, center):
    changed = []
    for frame in particles:
        frame = frame.assign(x_scale=frame['x']-center[0])
        frame = frame.assign(y_scale=frame['y']-center[1])
        frame = frame.assign(z_scale=frame['z']-center[2])
        changed.append(frame)
    return tuple(changed)



def main():
    """ tests compute_center() """
    data_file = "low_res_1.dat"
    data4d, time_array = generate_4d_data(data_file)
    col_header = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'iwas', 'id', 'mass']
    old, new, gas, gal = convert_to_pd(col_header, data4d)
    center = data4d[-1][3][0, 0:3]
    particles = (old, new, gas, gal)
    compute_center(particles, center)
    particles_submit = compute_center(particles, center)
    plt1 = individual_particles(data4d, particles_submit)
    plt1.show()


if __name__ == "__main__":
    main()
