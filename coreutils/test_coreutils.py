#!/usr/bin/env python

from __future__ import print_function
import os, sys
import subprocess, time
import signal

def main(argv):
    
    try:
        stdin_dir = sys.argv[1]+ "reading_from_stdin/"
        file_dir = sys.argv[1] + "reading_from_file/"
        num_of_cores = int(sys.argv[2]) # the number of cores of the system as command line arg
        fuzz_time = int(sys.argv[3]) # define how much time (in sec) should the fuzzer for each process
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise
    sync_dir = "sync_dir" # the root folder where all instances will store their results
    if not os.path.exists(sync_dir):
        os.makedirs(sync_dir)
    path_to_target = "../src/./" # path to the executables
    counter = 1;
    pids = [] # list to store the pids of all the subprocesses

    for filename in os.listdir(stdin_dir): # first fuzz the programs reading from stdin
        if not filename.startswith('.' or '..'):
            testcase_dir = stdin_dir + filename + "/testcases/"
            target_sync_dir = sync_dir + "/" + filename
            fuzzed_binary = path_to_target + filename
            fuzzed_instance = filename + str(counter) #sync id of the instance
            # master
            args = ["afl-fuzz", "-i", testcase_dir, "-o", target_sync_dir, "-M", fuzzed_instance, fuzzed_binary]
            proc = subprocess.Popen(args)
            pids.append(proc.pid)
 
            for i in range(1, num_of_cores):
                counter += 1
                fuzzed_instance = filename + str(counter)
                # slaves
                args = ["afl-fuzz", "-i", testcase_dir, "-o", target_sync_dir, "-S", fuzzed_instance, fuzzed_binary]
                proc = subprocess.Popen(args)
                pids.append(proc.pid)

            time.sleep(fuzz_time) # suspend the main process 
            for pid in pids:
                os.kill(pid, signal.SIGKILL) # kill all the subprocesses generated and fuzz the next program
            pids = []
            counter = 1

    for filename in os.listdir(file_dir): # fuzz the programs reading from file 
        if not filename.startswith('.' or '..'):
            testcase_dir = file_dir + filename + "/testcases/"
            target_sync_dir = sync_dir + "/" + filename
            fuzzed_binary = path_to_target + filename
            fuzzed_instance = filename + str(counter)
            args = ["afl-fuzz", "-i", testcase_dir, "-o", target_sync_dir, "-M", fuzzed_instance, fuzzed_binary, "@@"]
            proc = subprocess.Popen(args)
            pids.append(proc.pid)

            for i in range(1, num_of_cores):
                counter += 1
                fuzzed_instance = filename + str(counter)
                args = ["afl-fuzz", "-i", testcase_dir, "-o", target_sync_dir, "-S", fuzzed_instance, fuzzed_binary, "@@"]
                proc = subprocess.Popen(args)
                pids.append(proc.pid)

            time.sleep(fuzz_time)
            for pid in pids:
                os.kill(pid, signal.SIGKILL)
            pids = []
            counter = 1
                   
    return 1
     
if __name__ == '__main__':
    main(sys.argv[1:])
