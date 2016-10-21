from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from Photon import Photon
from Grids import Grids
from Layer import Layer
import time
np.set_printoptions(threshold=np.inf)

# set parameters
ly1 = Layer(z0=-1, z1=0, mu_a=0, mu_s=0, g=1, n=1, clear=True, ambient=True)
ly2 = Layer(z0=0, z1=np.inf, mu_a=0.1, mu_s=100, g=0.9, n=1, clear=False, ambient=False)
ly3 = Layer(z0=np.inf, z1=np.inf, mu_a=0, mu_s=0, g=1, n=1, clear=True, ambient=True)
ly_ls = [ly1, ly2, ly3]
n_photon = 100
w_thresh = 0.0001
m = 10
n_r = 500 # number of grid pixels along r
n_z = 200 # number of grid pixels along z
delta_r = 0.005
delta_z = 0.005

##
# set recording grids
out_grids = Grids(n_r, delta_r, n_z, delta_z)

## 
# get random seed
cpu_time = time.time() * 10000 % 10000
np.random.seed(seed=int(cpu_time))

# start loop
for i_photon in range(n_photon):
    
    print('\r{:d}/{:d}'.format(i_photon+1, n_photon), end='')
    
    # initialize
    ph = Photon(0, 0, ly_ls)

    while not ph.dead:
        
        # set new s if s = 0
        if ph.s == 0:
            ph.get_s()

        # check boundary and move
        ph.move(ly_ls)

        # if no booundary hit, absorb and scatter
        if ph.s == 0:
            dw = ph.absorb(ly_ls)
            out_grids.update_a(ph, dw)
            ph.scatter(ly_ls)
        # if boundary hit, transmit or reflect
        else:
            ph.reflect_transmit(ly_ls)

        # if photon is alive but low in weight, run roulette
        if not ph.dead:
            if ph.w < w_thresh:
                ph.terminate(m)
    
##
# post-processing
phi_z = out_grids.get_phiz(ly_ls, n_photon)
z_coords = out_grids.get_zcoords()
fname = 'phiz_n_{:d}_ri_{:.2f}'.format(n_photon, ly2.n)
np.save(fname, phi_z)

##
# plot
fig = plt.figure()
plt.semilogy(z_coords[:-1], phi_z[:-1])
plt.xlabel('z [cm]')
plt.ylabel('Fluence')
plt.title('Fluence vs. depth (N = {:d}, n = {:.2f})'.format(n_photon, ly2.n))
fname = 'n_{:d}_ri_{:.2f}.tiff'.format(n_photon, ly2.n)
plt.savefig(fname)
