import numpy as np
from collections import Counter
import time
from parameters import *
from main import filename, log


class NetworkTask2:

    def __init__(self):

        self.data, self.n_line, self.n_node = self.load_data()
        self.k_out = self.build_degree()
        self.dangling = self.build_dangling()
        self.p = self.build_gp()
        self.k = self.build_index()

    def load_data(self) -> int:

        start = time.time()
        data = np.loadtxt("data/" + filename + ".txt", dtype=int)
        n_line = len(self.data)

        n_node = 0
        for i in data:
            for j in i:
                if j > n_node:
                    n_node = j

        end = time.time()

        log_string = "Data loaded in {:4f} s".format(end - start)
        print(log_string)
        log.write(log_string)

        return data, int(n_line), int(n_node)

    def build_degree(self) -> dict:

        start = time.time()

        k_out = Counter(self.data[:, 0])

        end = time.time()
        log_string = "k_out built in {:.6f} s".format(end - start)
        print(log_string)
        log.write(log_string)

        return dict(k_out)

    def build_dangling(self) -> np.ndarray:

        start = time.time()
        dangling = []
        dang = set(self.k_out)

        for i in range(self.n_node):
            if i + 1 not in dang:
                dangling.append(i + 1)

        end = time.time()

        log_string = "Dangling nodes array built in " \
                     "{:.6f} ms".format(100 * (end - start))
        print(log_string)
        log.write(log_string)

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

            for i in self.dangling:
                gp += alpha * p[i - 1] / self.n_node

            gp += (1 - alpha) / self.n_node

            gp = gp / np.linalg.norm(gp, 1)

            if np.linalg.norm(gp - p) < epsilon:
                print("Done in {} iterations".format(counter))
                break
            elif counter >= 1000:
                print("Limit reached")
                break

        end = time.time()
        log_string = "Steady state probability array built " \
                     "in {:.6f} s".format(end - start)
        print(log_string)
        log.write(log_string)

        return p

    def build_index(self) -> np.ndarray:

        start = time.time()

        dtype = [('node', int), ('rank', float)]
        k = []

        for i in range(self.n_node):
            k.append((i + 1, self.p[i]))

        k = np.array([tuple(row) for row in k], dtype=dtype)
        k = np.flip(np.sort(k, order='rank'))
        for i in range(self.n_node):
            k['rank'][i] = i + 1

        end = time.time()
        log_string = "Array sorted in {:.6f} s".format(end - start)
        print(log_string)
        log.wite(log_string)

        dtype = [('node', 'int'), ('rank', 'int')]
        k = np.array(k, dtype=dtype)

        np.savetxt(filename + "_out.dat", k, fmt='%i')

        return k
