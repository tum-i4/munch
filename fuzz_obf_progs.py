#!/usr/bin/env python3

import os, sys
import subprocess, time, signal
import glob

def main(argv):
 
    try:
        obf_dir = sys.argv[1] # name of the dir with the patched obf progs
        testcases = sys.argv[2] # testcases for the program used by afl-fuzz
        fuzz_time = int(sys.argv[3]) # time to run afl-fuzzer
        num_of_cores = int(sys.argv[4]) # the number of cores of the system as command line arg
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise
        
    sync_dir = "sync_dir" # the root folder where all instances will store their results
    if not os.path.exists(obf_dir + "/" + sync_dir):
        os.makedirs(obf_dir + "/" + sync_dir)
    
    counter = 1
    pids = []
    for filename in glob.glob(obf_dir+"/*_afl.c"):
        if not filename.startswith('.' or '..'):
            # 1. compile the patched obfuscated prog with afl-gcc
            afl_binary = filename[:-2] + "_bin"
            args = ["afl-gcc", filename, "-o", afl_binary] # creates the instrumented binary to fuzz with afl
            subprocess.call(args)
    
            # 2. run the afl binary with afl-fuzz
            target_sync_dir = os.path.dirname(filename) + "/" + sync_dir + "/" + os.path.basename(filename[:-2])
            fuzzed_binary = afl_binary
            fuzzed_instance = str(counter) #sync id of the instance
            # master
            args = ["afl-fuzz", "-i", testcases, "-o", target_sync_dir, "-M", fuzzed_instance, fuzzed_binary]
            proc = subprocess.Popen(args)
            pids.append(proc.pid)

            for i in range(1, num_of_cores):
                counter += 1
                fuzzed_instance = str(counter)
                # slaves
                args = ["afl-fuzz", "-i", testcases, "-o", target_sync_dir, "-S", fuzzed_instance, fuzzed_binary]
                proc = subprocess.Popen(args)
                pids.append(proc.pid)

            time.sleep(fuzz_time) # suspend the main process 
            for pid in pids:
                os.kill(pid, signal.SIGKILL) # kill all the subprocesses generated and fuzz the next program
            pids = []
            counter = 1
    
if __name__ == '__main__':
    main(sys.argv[1:])
