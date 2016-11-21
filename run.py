from __future__ import print_function
import numpy as np
import time
from Photon import *


def run_mc(n_photon, ly_ls, out_grids, w_thresh, m):

    # get random seed
    cpu_time = time.time() * 10000 % 10000
    np.random.seed(seed=int(cpu_time))

    # start loop
    t0 = time.time()
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

    t = time.time() - t0
    print('\nMC Done in {:.2f} s ({:.2f} hours). '.format(t, t/3600))