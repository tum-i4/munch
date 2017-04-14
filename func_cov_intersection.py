import os, sys
import subprocess, time
import glob

def main(argv):
    print(argv)
    try:
        llvm_path = argv[0]
        afl_path = argv[1]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # set of AFL functions
    afl_cov_file = open(afl_path+'/covered_functions.txt')
    afl_set = set()

    for line in afl_cov_file:
        afl_set.add(line.strip())

    # set of KLEE functions
    klee_cov_file = open(llvm_path + '/covered_funcs_klee_full.txt')
    klee_set = set()

    for line in klee_cov_file:
        klee_set.add(line.strip())


    both_cov = afl_set.intersection(klee_set)
    print(both_cov)
    print(len(both_cov))

if __name__ == '__main__':
    main(sys.argv[1:])

