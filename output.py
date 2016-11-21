from __future__ import print_function
from paras import *
import numpy as np
import matplotlib.pyplot as plt


def get_z_fluence(out_grids):

    # post-processing
    phi_z = out_grids.get_phiz(ly_ls, n_photon)
    z_coords = out_grids.get_zcoords()
    fname = 'phiz_n_{:d}_ri_{:.2f}'.format(n_photon, ly2.n)
    np.save(fname, phi_z)

    # plot
    fig = plt.figure()
    plt.semilogy(z_coords[:-1], phi_z[:-1])
    plt.xlabel('z [cm]')
    plt.ylabel('Fluence')
    plt.title('Fluence vs. depth (N = {:d}, n = {:.2f})'.format(n_photon, ly2.n))
    fname = 'n_{:d}_ri_{:.2f}.png'.format(n_photon, ly2.n)
    plt.savefig(fname)


def get_xz_fluence(out_grids):

    phi_xz = out_grids.get_phixz(ly_ls)
    z_coords = out_grids.get_zcoords()

    plt.figure()
    plt.imshow(phi_xz[:-1, 1:-1])
    fname = 'xz_abs.png'.format(n_photon, ly2.n)
    plt.savefig(fname)

