import numpy as np
from parameters import *


class NetworkTask2:

    def __init__(self):

        self.data = np.loadtxt(filename)
        self.n_line = len(self.data)
        self.n_node = self.get_node_number()
        self.structure = self.build_network_structure()
        self.k_in = self.build_degree()[0]
        self.k_out = self.build_degree()[1]
        self.dangling = self.build_dangling()
        self.stochastic = self.build_stochastic_array()
        self.google = self.build_google_array()
        self.foo = False

    def get_node_number(self) -> int:

        n_node = 0
        for i in self.data:
            for j in i:
                if j > n_node:
                    n_node = j

        return int(n_node)

    def build_network_structure(self) -> np.ndarray:

        structure = []

        for i in self.data:
            start_node = int(i[0] - 1)
            end_node = int(i[1] - 1)
            structure.append((1, end_node, start_node))

        return np.array(structure, dtype=int)

    def build_degree(self) -> tuple[np.ndarray, np.ndarray]:

        k_in = np.zeros(self.n_node, dtype=int)
        k_out = np.zeros(self.n_node, dtype=int)

        for i in range(self.n_node):
            for j in self.structure:
                if j[2] == i:
                    k_out[i] += 1
                if j[1] == i:
                    k_in[i] += 1

        return k_in, k_out

    def build_dangling(self) -> np.ndarray:

        dangling = []

        for i in range(self.n_node):
            if self.k_out[i] == 0:
                dangling.append(i)

        return np.array(dangling, dtype=int)

    def build_stochastic_array(self) -> np.ndarray:

        stochastic = []

        for i in self.structure:
            stochastic.append((1 / self.k_out[i[2]], i[1], i[2]))
        for i in self.dangling:
            for j in range(self.n_node):
                stochastic.append((1 / self.n_node, j, i))

        return np.array(stochastic, dtype=float)

    def build_google_array(self) -> np.ndarray:

        google = []



        return google
