import numpy as np


class Photon():

    def __init__(self, x, y, ly_ls):
        # initialize photon
        self.x = x
        self.y = y
        self.z = 0
        self.ux = 0
        self.uy = 0
        self.uz = 1
        self.dead = False
        self.s = 0
        self.scatters = 0
        self.layer = 1
        # in case that first layer is clear, do reflection
        amb_ly = ly_ls[0]
        this_ly = ly_ls[1]
        bot_ly = ly_ls[2]
        n1 = amb_ly.n
        n2 = this_ly.n
        n3 = bot_ly.n
        if this_ly.clear:
            r1 = ((n1 - n2) / (n1 + n2)) ** 2
            r2 = ((n3 - n2) / (n3 + n2)) ** 2
            r_sp = r1 + (1 - r1) ** 2 * r2 / (1 - r1 * r2)
            self.w = 1 - r_sp
        else:
            if n1 != n2:
                r_sp = ((n1 - n2) / (n1 + n2)) ** 2
                self.w = 1 - r_sp
            else:
                self.w = 1

    def get_s(self):
        # get random s
        xi = np.random.rand()
        self.s = -np.log(xi)

    def absorb(self, ly_ls):
        # deduce weight due to absorption
        this_ly = ly_ls[self.layer]
        mu_ratio = this_ly.mu_a / this_ly.mu_t
        delta_w = self.w * mu_ratio
        self.w -= delta_w
        return delta_w

    def scatter(self, ly_ls):
        # update direction cosines upon scattering
        xi = np.random.rand()
        this_ly = ly_ls[self.layer]
        g = this_ly.g
        if g != 0:
            cosine = 1 + g ** 2 - ((1 - g ** 2) / (1 - g + 2 * g * xi)) ** 2
            cosine /= (2 * g)
        else:
            cosine = 2 * xi - 1
        theta = np.arccos(cosine)
        xi = np.random.rand()
        phi = 2 * np.pi * xi
        mux = self.ux
        muy = self.uy
        muz = self.uz
        if np.abs(muz) < 0.99999:
            self.ux = np.sin(theta) * (mux * muz * np.cos(phi) - muy * np.sin(phi))
            self.ux = self.ux / np.sqrt(1 - muz ** 2) + mux * cosine
            self.uy = np.sin(theta) * (muy * muz * np.cos(phi) + mux * np.sin(phi))
            self.uy = self.uy / np.sqrt(1 - muz ** 2) + muy * cosine
            self.uz = -np.sin(theta) * np.cos(phi) * np.sqrt(1 - muz ** 2) + muz * cosine
        else:
            self.ux = np.sin(theta) * np.cos(phi)
            self.uy = np.sin(theta) * np.sin(phi)
            self.uz = np.sign(muz) * cosine
        self.scatters += 1

    def move(self, ly_ls):
        # judge if the photon will hit boundary then move it
        this_ly = ly_ls[self.layer]
        mu_t = this_ly.mu_t
        z_bound = [this_ly.z0, this_ly.z1]
        if self.uz < 0:
            db = (z_bound[0] - self.z) / self.uz
        elif self.uz == 0:
            db = np.inf
        else:
            db = (z_bound[1] - self.z) / self.uz
        if db * mu_t <= self.s:
            # hit boundary
            self.x += self.ux * db
            self.y += self.uy * db
            self.z += self.uz * db
            self.s -= db * mu_t
        else:
            # does not hit boundary
            self.x += self.ux * self.s / mu_t
            self.y += self.uy * self.s / mu_t
            self.z += self.uz * self.s / mu_t
            self.s = 0

    def reflect_transmit(self, ly_ls):
        # do reflection or transmission
        this_ly = ly_ls[self.layer]
        a_i = np.arccos(np.abs(self.uz))
        n_i = this_ly.n
        if self.uz < 0:
            next_ly = ly_ls[self.layer - 1]
            direct = -1
        else:
            next_ly = ly_ls[self.layer + 1]
            direct = 1
        n_t = next_ly.n
        a_t = np.arcsin(n_i * np.sin(a_i) / n_t)
        if n_i > n_t and a_i > np.arcsin(n_t / n_i):
            r = 1
        else:
            r = (np.sin(a_i - a_t) / np.sin(a_i + a_t)) ** 2 + (np.tan(a_i - a_t) / np.tan(a_i + a_t)) ** 2
            r *= 0.5
        xi = np.random.rand()
        if xi <= r:
            # internally reflected
            self.uz = -self.uz
        else:
            # transmitted
            if direct == -1:
                self.layer = self.layer - 1
            else:
                self.layer = self.layer + 1
            if self.layer == 0 or self.layer == len(ly_ls) - 1:
                self.dead = True
            else:
                self.ux = self.ux * n_i / n_t
                self.uy = self.uy * n_i / n_t
                self.uz = np.sign(self.uz) * np.cos(a_t)

    def terminate(self, m):
        xi = np.random.rand()
        if xi <= 1 / m:
            self.w = m * self.w
        else:
            self.w = 0
            self.dead = True
