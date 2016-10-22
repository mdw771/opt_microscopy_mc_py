import numpy as np
import matplotlib.pyplot as plt
from Grids import *


n_r = 500 # number of grid pixels along r
n_z = 200 # number of grid pixels along z
delta_r = 0.005
delta_z = 0.005

out_grids = Grids(n_r, delta_r, n_z, delta_z)

for n in [1000, 10000, 100000, 1000000]:
    fig = plt.figure()
    n100 = np.load('phiz_n_{:d}_ri_1.00.npy'.format(n))
    n137 = np.load('phiz_n_{:d}_ri_1.37.npy'.format(n))
    z = out_grids.get_zcoords()
    plt.semilogy(z, n100, z, n137)
    plt.ylim([1e-1, 1e1])
    plt.savefig('comb_n_{:d}'.format(n))

