class Layer():

    def __init__(self, z0, z1, mu_a, mu_s, g, n, clear, ambient):
        self.z0 = z0
        self.z1 = z1
        self.mu_a = mu_a
        self.mu_s = mu_s
        self.mu_t = mu_a + mu_s
        self.g = g
        self.n = n
        self.clear = clear
        self.ambient = ambient
