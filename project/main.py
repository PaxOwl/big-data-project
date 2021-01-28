#! /bin/python3

import functions_task1 as fc1
import functions_task2 as fc2
import time
import numpy as np


# print("---------- Part 1 ----------")
# t_init = time.time()
# network1 = fc1.NetworkTask1()
# t_end = time.time()
# print("Elapsed time for part 1: {:.6f} seconds.".format(t_end - t_init))
# print("The ranking for the input data is as follows:")
# print("Node", "Rank")
# for i in range(network1.n_node):
#     print(i + 1, '  ', network1.k[i])

print("\n---------- Part 2 ----------")
t_init = time.time()
network2 = fc2.NetworkTask2()
t_end = time.time()
print("Elapsed time for part 2: {:.6f} seconds.".format(t_end - t_init))
print("The ranking for the input data is as follows:")
print("Node", "Rank")
for i in range(10):
    print(i + 1, '  ', network2.k[i])

