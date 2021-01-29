#! /bin/python3

import functions_task1 as fc1
import functions_task2 as fc2
import time
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
    t_end = time.time()
    print("Elapsed time for part 2: {:.6f} seconds.".format(t_end - t_init))
    print("The ranking for the input data is as follows:")
    print("Node", "Rank")
    for i in range(network2.n_node):
        print(network2.k['node'][i], '  ', network2.k['rank'][i])
        if i == 9:
            break

else:
    # files = ["arwiki", "dawiki", "dewiki", "elwiki",
    #          "enwiki", "eswiki", "fawiki", "frwiki",
    #          "hewiki", "hiwiki", "huwiki", "itwiki",
    #          "jawiki", "kowiki", "mswiki", "nlwiki",
    #          "plwiki", "ptwiki", "ruwiki", "svwiki",
    #          "thwiki", "trwiki", "viwiki", "zhwiki"]
    for f in files:
        with open("data_out/" + f + ".log", "w") as logfile:
            t_start = time.time()
            start_string = "Started computation for {}".format(f)
            print(start_string)
            logfile.write(start_string)
            data = fc2.NetworkTask2()
            data.compute(f)
            logfile.write(data.log)
            t_end = time.time()
            end_string = "\nComputation ended for {}. " \
                         "Time elapsed: {:.4} s".format(f, t_end - t_start)
            print(end_string)
            logfile.write(end_string)
