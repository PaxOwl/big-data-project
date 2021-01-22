import numpy as np
from parameters import *


class NetworkTask2:

    def __init__(self):

        self.data = self.init_data()
        self.n_line = len(self.data)
        self.n_node = self.get_node_number()
        self.structure = self.build_network_structure()
        self.k_in = self.build_degree()[0]
        self.k_out = self.build_degree()[1]
        self.dangling = self.build_dangling()
        self.stochastic = self.build_stochastic_list()
        self.google = self.build_google_list()
        self.foo = False

    @staticmethod
    def init_data() -> list[tuple[int, int]]:

        data = np.loadtxt(filename)
        new_data = []
        for i in range(len(data)):
            new_data.append((int(data[i, 0]), int(data[i, 1])))

        return new_data

    def get_node_number(self) -> int:

        n_node = 0
        for i in self.data:
            for j in i:
                if j > n_node:
                    n_node = j

        return n_node

    def build_network_structure(self) -> list[tuple[int, int, int]]:

        structure = []

        for i in self.data:
            start_node = int(i[0] - 1)
            end_node = int(i[1] - 1)
            structure.append((1, end_node, start_node))

        return structure

    def build_degree(self) -> tuple[list[int], list[int]]:

        k_in = list(np.zeros(self.n_node, dtype=int))
        k_out = list(np.zeros(self.n_node, dtype=int))

        for i in range(self.n_node):
            for j in self.structure:
                if j[2] == i:
                    k_out[i] += 1
                if j[1] == i:
                    k_in[i] += 1

        return k_in, k_out

    def build_dangling(self) -> list[int]:

        dangling = []

        for i in range(self.n_node):
            if self.k_out[i] == 0:
                dangling.append(i)

        return dangling

    def build_stochastic_list(self) -> list[tuple[float, int, int]]:

        stochastic = []

        for i in self.structure:
            stochastic.append((1 / self.k_out[i[2]], i[1], i[2]))
        for i in self.dangling:
            for j in range(self.n_node):
                stochastic.append((1 / self.n_node, j, i))

        return stochastic

    # def build_google_list(self) -> list[float]:
    #
    #     google = []
    #
    #
    #
    #     return google

