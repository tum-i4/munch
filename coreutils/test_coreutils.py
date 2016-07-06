#!/usr/bin/env python

import os, sys
import subprocess

def main():
    sync_dir = "sync_dir" # the shared folder where all the instances will store the results
    stdin_dir = sys.argv[1]+ "reading_from_stdin/"
    file_dir = sys.argv[1] + "reading_from_file/"
    path_to_target = "../src/./"
    for filename in os.listdir(stdin_dir):
        if not filename.startswith('.' or '..'):
            testcase_dir = stdin_dir + filename + "/testcases/"
            fuzzed_binary = path_to_target + filename
            args = ["afl-fuzz", "-i " + testcase_dir, "-o " + sync_dir, "-S " + filename, fuzzed_binary]
            # os.execvp("afl-fuzz", args)
            subprocess.Popen(args)

    for filename in os.listdir(file_dir):
        if not filename.startswith('.' or '..'):
            testcase_dir = file_dir + filename + "/testcases/"
            fuzzed_binary = path_to_target + filename
            args = ["afl-fuzz", "-i " + testcase_dir, "-o " + sync_dir, "-S " + filename, fuzzed_binary, "@@"]
            # os.execvp("afl-fuzz", args)
            subprocess.Popen(args)
                   
    return 1
     
if __name__ == '__main__':
    main()