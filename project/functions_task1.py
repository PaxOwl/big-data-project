import numpy as np
from parameters1 import *


class NetworkTask1:

    def __init__(self):

        self.data = np.loadtxt("data/" + filename + ".txt")
        self.n_line = len(self.data)
        self.n_node = int(np.max(self.data))
        self.structure = self.build_network_structure()
        self.stochastic = self.build_stochastic_matrix()
        self.google = self.build_google_matrix()
        self.p_zero = self.initial_probability(j0)
        self.ssp = self.steady_state_probability()
        self.k = self.sort_nodes()

    def build_network_structure(self) -> np.ndarray:

        structure = np.zeros((self.n_node, self.n_node), dtype=int)

        for i in range(self.n_line):
            start_node = int(self.data[i, 1] - 1)
            end_node = int(self.data[i, 0] - 1)
            structure[start_node, end_node] = 1

        return structure

    def build_stochastic_matrix(self) -> np.ndarray:

        stochastic = np.zeros((self.n_node, self.n_node), dtype=float)
        k_in = np.zeros((self.n_node, 1), dtype=float)
        k_out = np.zeros((self.n_node, 1), dtype=float)

        for j in range(self.n_node):
            for i in range(self.n_node):
                k_in[j] += self.structure[j, i]
                k_out[j] += self.structure[i, j]

        for i in range(self.n_node):
            for j in range(self.n_node):
                if k_out[j] == 0:
                    stochastic[i, j] = 1. / float(self.n_node)
                else:
                    stochastic[i, j] = self.structure[i, j] / k_out[j]

        return stochastic

    def build_google_matrix(self) -> np.ndarray:

        v = np.zeros((self.n_node, 1))
        g = np.zeros((self.n_node, self.n_node))

        for i in range(self.n_node):
            v[i] = 1 / self.n_node
            for j in range(self.n_node):
                g[i, j] = alpha * self.stochastic[i, j] + (1 - alpha) * v[i]

        return g

    def initial_probability(self, j0) -> np.ndarray:

        p_zero = np.zeros(self.n_node, dtype=int)

        for i in range(self.n_node):
            p_zero[i] = kronecker(i + 1, j0)

        return p_zero

    def steady_state_probability(self) -> np.ndarray:

        epsilon = 10**(-4)

        p_temp = self.p_zero
        counter = 0

        while "Not equal":
            counter += 1
            p = p_temp
            p_temp = np.matmul(self.google, p)
            
            if (abs(p - p_temp) <= epsilon * np.ones((self.n_node, 1))).all():
                print("Done in {} iterations".format(counter))
                break
            elif counter >= 10000:
                print("Limit reached")
                break
        return p

    def sort_nodes(self) -> np.ndarray:

        k = np.empty(self.n_node, dtype=int)
        temp_ssp = self.ssp.copy()

        for i in range(self.n_node):
            counter = 1
            for j in range(self.n_node):
                if temp_ssp[i] < temp_ssp[j]:
                    counter += 1
            k[i] = counter

        return k


def kronecker(i: float, j: float) -> int:

    if i == j:
        return 1
    else:
        return 0
