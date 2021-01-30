import numpy as np
from collections import Counter
import time
from parameters2 import *


class NetworkTask2:

    def __init__(self):
        """
        Initiates the data
        """
        self.data = None
        self.n_line = None
        self.n_node = None
        self.k_out = None
        self.dangling = None
        self.ssp = None
        self.k = None
        self.log = ""

    def compute(self, filename: str):
        """
        Calls the different functions to compute the attributes of the class

        :param filename: Name of the file to use
        """
        self.data, self.n_node = self.load_data(filename)
        self.k_out = self.build_degree()
        self.dangling = self.build_dangling()
        self.ssp = self.build_p(filename)
        self.k = self.build_index(filename)

    def load_data(self, filename: str) -> tuple[np.ndarray, int]:
        """
        Reads the input file and stores its data in an array

        :param filename: Name of the file to use
        :return: Data of the input file and number of nodes
        """
        start = time.time()
        data = np.loadtxt("data/" + filename + ".txt", dtype=int)

        n_node = 0
        for i in data:
            for j in i:
                if j > n_node:
                    n_node = j

        end = time.time()

        log_string = "\nData loaded in {:.4f} s".format(end - start)
        print(log_string)
        self.log = self.log + log_string

        return data, int(n_node)

    def build_degree(self) -> dict:
        """
        Builds the dictionary of ways out for each node

        :return: The number of ways out for each node
        """
        start = time.time()

        k_out = Counter(self.data[:, 0])

        end = time.time()
        log_string = "\nk_out built in {:.4f} ms".format(1000 * (end - start))
        print(log_string)
        self.log = self.log + log_string

        return dict(k_out)

    def build_dangling(self) -> np.ndarray:
        """
        Using the dictionary k_out, builds the array of dangling nodes

        :return: Array containing all the dangling nodes of the network
        """
        start = time.time()
        dangling = []
        dang = set(self.k_out)

        for i in range(self.n_node):
            if i + 1 not in dang:
                dangling.append(i + 1)

        end = time.time()

        log_string = "\nDangling nodes array built in " \
                     "{:.4f} ms".format(1000 * (end - start))
        print(log_string)
        self.log = self.log + log_string

        return np.array(dangling, dtype=int)

    def build_p(self, filename: str) -> np.ndarray:
        """
        Builds the steady state probability list of the network

        :param filename: Name of the file to use
        :return: Steady state probability array
        """
        start = time.time()

        gp = np.array([1 / self.n_node for _ in range(self.n_node)],
                      dtype=float)

        counter = 0
        t_init = time.time()
        while True:
            counter += 1
            t_iter = time.time()
            print("{}: iteration {}, {:.4f} s".format(filename, counter,
                                                      t_iter - t_init))
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
        log_string = "\nSteady state probability array built " \
                     "in {:.4f} s, {} iterations".format(end - start, counter)
        print(log_string)
        self.log = self.log + log_string

        return p

    def build_index(self, filename: str) -> np.ndarray:
        """
        Sorts and ranks the nodes given the steady state probability array
        self.ssp

        :param filename: Name of the file to use
        :return: Nodes of the network with associated rank
        """
        start = time.time()

        dtype = [('node', int), ('rank', float)]
        k = []

        for i in range(self.n_node):
            k.append((i + 1, self.ssp[i]))

        k = np.array([tuple(row) for row in k], dtype=dtype)
        k = np.flip(np.sort(k, order='rank'))
        for i in range(self.n_node):
            k['rank'][i] = i + 1

        end = time.time()
        log_string = "\nArray sorted in {:.4f} ms".format(1000 * (end - start))
        print(log_string)
        self.log = self.log + log_string

        dtype = [('node', 'int'), ('rank', 'int')]
        k = np.array(k, dtype=dtype)

        np.savetxt("data_out/" + filename + "_out.dat", k, fmt='%i')

        return k
