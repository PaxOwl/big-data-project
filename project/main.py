#! /bin/python3

import functions_task1 as fc1
import functions_task2 as fc2
import time

t_init = time.time()
network1 = fc1.NetworkTask1()
t_end = time.time()
print("Elapsed time for part 1: {:.3f} seconds.".format(t_end - t_init))
print("The ranking for the input data is as follows:")
print("Node", "Rank")
for i in range(network1.n_node):
    print(i + 1, '  ', network1.k[i])

t_init = time.time()
network2 = fc2.NetworkTask2()
t_end = time.time()
