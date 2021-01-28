import numpy as np
from collections import Counter
import time
from parameters import *


class NetworkTask2:

    def __init__(self):

        self.data = np.loadtxt("data/" + filename + ".txt", dtype=int)
        self.n_line = len(self.data)
        self.n_node = self.get_node_number()
        self.k_out = self.build_degree()
        self.dangling = self.build_dangling()
        self.p = self.build_gp()
        self.k = self.sort_nodes()

    def get_node_number(self) -> int:

        start = time.time()

        n_node = 0
        for i in self.data:
            for j in i:
                if j > n_node:
                    n_node = j

        end = time.time()
        print("Node number retrieved in {:6f} s".format(end - start))

        return int(n_node)

    def build_degree(self) -> dict:

        start = time.time()

        k_out = Counter(self.data[:, 0])

        end = time.time()
        print("k_out built in {:.6f} s".format(end - start))

        return dict(k_out)

    def build_dangling(self) -> np.ndarray:

        start = time.time()
        dangling = []
        dang = set(self.k_out)

        for i in range(self.n_node):
            if i + 1 not in dang:
                dangling.append(i + 1)

        end = time.time()
        print("dangling nodes array built in {:.6f} s".format(end-start))

        return np.array(dangling, dtype=int)

    def build_gp(self) -> np.ndarray:

        start = time.time()

        epsilon = 10 ** (-4)
        gp = np.array([1 / self.n_node for _ in range(self.n_node)],
                      dtype=float)

        counter = 0
        while True:
            counter += 1
            p = gp.copy()
            for i in self.data:
                gp[i[1] - 1] += alpha * p[i[0] - 1] / self.k_out[i[0]]

            for i in range(self.n_node):
                gp[i] += (1 - alpha) / self.n_node

            for i in self.dangling:
                gp += alpha * p[i - 1] / self.n_node

            gp = gp / np.linalg.norm(gp, 1)

            if np.linalg.norm(gp - p) < epsilon:
                print("Done in {} iterations".format(counter))
                break
            elif counter >= 1000:
                print("Limit reached")
                break

        end = time.time()
        print("Steady state probability array built "
              "in {:.6f} s".format(end - start))

        return p

    def sort_nodes(self) -> np.ndarray:

        start = time.time()

        k = np.empty(self.n_node, dtype=int)

        for i in range(self.n_node):
            counter = 0
            for j in self.p:
                if self.p[i] < j:
                    counter += 1
            k[i] = 1 + counter

        end = time.time()
        print("Array sorted in {:.6f} s".format(end - start))

        out = np.empty((self.n_node, 2), dtype=int)

        for i in range(self.n_node):
            out[i, 0] = i + 1
            out[i, 1] = k[i]

        np.savetxt(filename + "_out.dat", out, fmt='%i')

        return k
