#!/usr/bin/env python

import os, sys
import subprocess

def main(argv):

    # run afl-cov
    
    try:
        path_to_afl_results = sys.argv[1]    # dir with afl results
        src_file = sys.argv[2]  # src file
        bin_file = sys.argv[3]  # target binary compiled with gcov
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    code_dir = "."
    output = path_to_afl_results + "/" + src_file[:-2] + "_cov.txt"
    command = bin_file + " < AFL_FILE"
    args = ["afl-cov", "-d", path_to_afl_results, "-e", command, "-c", code_dir, "--coverage-include-lines", "--src-file", src_file, "-O"]
    file_to_write = open(output, "w+")
    subprocess.call(args, stdout=file_to_write)
    file_to_write.close()

    # get function coverage
    cov_dir = path_to_afl_results + "/cov/"
    filename = cov_dir + "id-delta-cov"
    f_cov = open(filename, "r")
    next(f_cov)

    write_func = cov_dir + src_file[:-2] + "_func_cov.txt"
    f = open(write_func, "a+")

    for line in f_cov:
        words = line.split(" ")
        if "function" in words[3]:
            f.write(words[4][:-3] + "\n")

    f.close()
    f_cov.close()

    return 1

if __name__ == '__main__':
    main(sys.argv[1:])

