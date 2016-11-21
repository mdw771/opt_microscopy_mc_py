from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from Photon import Photon
from Grids import Grids
from Layer import Layer
from run import *
from output import *
from paras import *
import time

# set recording grids
out_grids = Grids(n_r, delta_r, n_z, delta_z)

# perform MC simulation
run_mc(n_photon, ly_ls, out_grids, w_thresh, m)

# output
# get_z_fluence(out_grids)
get_xz_fluence(out_grids)