import numpy as np

class Grids:

    def __init__(self, nr, delta_r, nz, delta_z):
        self.a_rz = np.zeros([nr, nz])
        self.a_xz = np.zeros([nz, 2*nr-1])
        self.delta_r = delta_r
        self.delta_z = delta_z
        self.nr = nr
        self.nz = nz
        self.rr = (nr-1)*delta_r
        self.zz = (nz-1)*delta_z

    def update_a(self, ph, dw):
        r = np.sqrt(ph.x**2 + ph.y**2)
        z = ph.z
        ir = int(r/self.delta_r)
        iz = int(z/self.delta_z)
        if ir >= self.nr-1 or ph.scatters == 0:
            ir = -1
        if iz >= self.nz-1:
            iz = -1
        self.a_rz[ir, iz] += dw
        if abs(ph.y < 2*self.delta_r):
            ix = int(ph.x/self.delta_r) + int(self.nr)
            if ix >= 2*self.nr-1:
                ix = -1
            elif ix < 0:
                ix = 0
            self.a_xz[iz, ix] += dw

    def get_az(self, n_photon):
        a_z = np.sum(self.a_rz, axis=0)
        a_z /= (self.delta_z*n_photon)
        return a_z

    def get_phiz(self, ly_ls, n_photon):
        zt = self.zz
        layer = 1
        a_z = self.get_az(n_photon)
        phi_z = np.zeros(self.nz)
        if len(ly_ls) == 3:
            this_ly = ly_ls[1]
            phi_z = a_z / this_ly.mu_a
        else:
            while zt > 0:
                this_ly = ly_ls[layer]
                thickness = this_ly.z1 - this_ly.z0
                iz0 = int(this_ly.z0/self.delta_z)
                if zt > thickness:
                    iz1 = int(this_ly.z1/self.delta_z)
                else:
                    iz1 = -1

                phi_z[iz0:iz1] = a_z[iz0:iz1]/this_ly.mu_a
                layer += 1
                zt -= thickness
        return phi_z

    def get_phixz(self, ly_ls):
        zt = self.zz
        layer = 1
        phi_xz = np.zeros(self.a_xz.shape)
        if len(ly_ls) == 3:
            this_ly = ly_ls[1]
            phi_xz = self.a_xz / this_ly.mu_a
        else:
            while zt > 0:
                this_ly = ly_ls[layer]
                thickness = this_ly.z1 - this_ly.z0
                iz0 = int(this_ly.z0/self.delta_z)
                # if this is not the final layer covered by scoring grid
                if zt > thickness:
                    iz1 = int(this_ly.z1/self.delta_z)
                # if this is the final layer covered by scoring grid
                else:
                    iz1 = -1
                phi_xz[iz0:iz1] = self.a_xz[iz0:iz1]/this_ly.mu_a
                layer += 1
                zt -= thickness
        return phi_xz

    def get_rcoords(self):
        i = np.arange(self.nr)
        r_coords = ((i+0.5)+1/(12*(i+0.5))) * self.delta_r
        return r_coords

    def get_xcoords(self):
        i = np.arange(2*self.nr-1)
        i = i + int(self.nr)
        x_coords = ((i+0.5)+1/(12*(i+0.5))) * self.delta_r
        return x_coords

    def get_zcoords(self):
        i = np.arange(self.nz)
        z_coords = (i+0.5) * self.delta_z
        return z_coords


