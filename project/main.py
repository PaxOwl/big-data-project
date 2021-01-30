#! /bin/python3

import functions_task1 as fc1
import functions_task2 as fc2
import time
from parameters1 import *
from parameters2 import run_all_files, files


if not run_all_files:
    print("---------- Part 1 ----------")
    t_init = time.time()
    network1 = fc1.NetworkTask1()
    t_end = time.time()
    print("Elapsed time for part 1: {:.6f} seconds.".format(t_end - t_init))
    print("The ranking for the input data is as follows:")
    print("Node", "Rank")
    for i in range(network1.n_node):
        print(i + 1, '  ', network1.k[i])

    print(network1.ssp)

    print("\n---------- Part 2 ----------")
    t_init = time.time()
    network2 = fc2.NetworkTask2()
    network2.compute(filename)
    t_end = time.time()
    print("Elapsed time for part 2: {:.6f} seconds.".format(t_end - t_init))
    print("The ranking for the input data is as follows:")
    print("Node", "Rank")
    for i in range(network2.n_node):
        print(network2.k['node'][i], '  ', network2.k['rank'][i])
        if i == 9:
            break

else:
    with open("data_out/logs.log", "w") as general_log:
        general_log.write("Starting computations at "
                          "{}\n".format(time.strftime("%H:%M")))
        for f in files:
            with open("data_out/" + f + ".log", "w") as logfile:
                t_start = time.time()
                start_string = "Started computation for {}".format(f)
                print(start_string)
                general_log.write("\n" + start_string)
                logfile.write(start_string)
                data = fc2.NetworkTask2()
                data.compute(f)
                general_log.write(data.log)
                logfile.write(data.log)
                t_end = time.time()
                end_string = "\nComputation ended for {}. Time " \
                             "elapsed: {:.4f} s".format(f, t_end - t_start)
                print(end_string)
                general_log.write(end_string)
                logfile.write(end_string)
        general_log.write("Computations ended at "
                          "{}".format(time.strftime("%H:%M")))
