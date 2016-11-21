from __future__ import print_function
from Grids import Grids
from Layer import Layer
from run import *

# set parameters
ly1 = Layer(z0=-1, z1=0, mu_a=0, mu_s=0, g=1, n=1, clear=True, ambient=True)
ly2 = Layer(z0=0, z1=np.inf, mu_a=0.1, mu_s=100, g=0.9, n=1.37, clear=False, ambient=False)
ly3 = Layer(z0=np.inf, z1=np.inf, mu_a=0, mu_s=0, g=1, n=1, clear=True, ambient=True)
ly_ls = [ly1, ly2, ly3]
n_photon = 1000
w_thresh = 0.0001
m = 10
n_r = 500 # number of grid pixels along r
n_z = 200 # number of grid pixels along z
delta_r = 0.005
delta_z = 0.005

# set recording grids
out_grids = Grids(n_r, delta_r, n_z, delta_z)