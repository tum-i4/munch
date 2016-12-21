#!/usr/bin/env python3

import os, sys
import subprocess, time, signal

def main(argv):
 
    try:
        obf_prog = sys.argv[1]    # name of the obfuscated program to patch
        testcases = sys.argv[2] # testcases for the program used by afl-fuzz
        fuzz_time = int(sys.argv[3]) # time to run afl-fuzzer
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise
        
    # 1. compile the patched obfuscated prog with afl-gcc
    afl_binary = obf_prog[:-2] + "_bin"
    args = ["afl-gcc", obf_prog, "-o", afl_binary] # creates the instrumented binary to fuzz with afl
    subprocess.call(args)

    # 2. run the afl binary with afl-fuzz
    afl_out_dir = obf_prog[:-2] + "_afl_out_res"
    afl_binary = "./" + afl_binary
    args = ["afl-fuzz", "-i", testcases, "-o", afl_out_dir, afl_binary]

    proc = subprocess.Popen(args)

    time.sleep(fuzz_time)
    os.kill(proc.pid, signal.SIGKILL)
    
if __name__ == '__main__':
    main(sys.argv[1:])

