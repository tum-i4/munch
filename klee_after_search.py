import os, sys
import subprocess, time
from collections import OrderedDict
import helper
import argparse
from os import path
import json
from pprint import pprint

AFL_OBJECT = ""
LLVM_OBJECT = ""
WHICH_KLEE = ""
AFL_FOLDER_NAME  = ""
SEARCH_NAME = ""
TARGET_INFO = ""
SYM_STDIN = ""
SYM_ARGS = ""
SYM_FILES = ""
FUNC_TIME = ""

#sys.path.append("/home/saahil/vdc")

def print_config():
    print("AFL_OBJECT: %s"%(AFL_OBJECT))
    print("LLVM_OBJECT: %s"%(LLVM_OBJECT))
    print("WHICH_KLEE: %s"%(WHICH_KLEE))
    print("AFL_FOLDER_NAME: %s"%(AFL_FOLDER_NAME))
    print("SEARCH_NAME: %s"%(SEARCH_NAME))
    print("TARGET_INFO: %s"%(TARGET_INFO))
    print("SYM_STDIN: %s SYM_ARGS: %s SYM_FILES: %s"%(SYM_STDIN, SYM_ARGS, SYM_FILES))
    print("FUNC_TIME: %s"%(FUNC_TIME))

""" Get configuration for after-search """
def read_config(config_file):
    json_file = open(config_file, "r")
    conf = json.load(json_file)

    global AFL_OBJECT, LLVM_OBJECT, WHICH_KLEE, AFL_FOLDER_NAME, SEARCH_NAME, TARGET_INFO, SYM_STDIN, SYM_ARGS, SYM_FILES, FUNC_TIME
    AFL_OBJECT = conf['AFL_OBJECT']
    LLVM_OBJECT = conf["LLVM_OBJECT"]
    WHICH_KLEE = conf["WHICH_KLEE"]
    AFL_FOLDER_NAME = conf["AFL_FOLDER_NAME"]
    SEARCH_NAME = conf["SEARCH_NAME"]
    TARGET_INFO = conf["TARGET_INFO"]
    SYM_STDIN = conf["SYM_STDIN"]
    SYM_ARGS = conf["SYM_ARGS"]
    SYM_FILES = conf["SYM_FILES"]
    FUNC_TIME = conf["FUNC_TIME"]

    print_config()

""" Returns afl function coverage """
def run_afl_cov(prog, afl_out_res):
    cov_dir = afl_out_res + "/cov/"
    filename = cov_dir + "id-delta-cov"
    with open(filename, "r") as f_cov:
        next(f_cov)

        func_list = []
        for line in f_cov:
            words = line.split(" ")
            if "function" in words[3]:
                func_list.append(words[4][:-3])

    return func_list

def run_klee_cov(prog, klee_out_res):
    covered = []

    istats = open(klee_out_res, "r")
    for line in istats:
        line = line.strip()
        if line.startswith("cfn="):
            func_name = line.split("=")[1]
            covered.append(func_name)

    return covered

def main(config_file):
    read_config(config_file)

    # get a list of functions topologically ordered
    all_funcs_topologic = helper.get_all_called_funcs(LLVM_OBJECT)
    print("Found %d functions in the program..."%len(all_funcs_topologic))
    #print("All functions:", all_funcs_topologic)

    #TODO: First run AFL here
    pos = AFL_OBJECT.rfind('/')
    afl_out_dir = AFL_OBJECT[:pos + 1] + AFL_FOLDER_NAME 
    func_list_afl = run_afl_cov(AFL_OBJECT, afl_out_dir)
    print("AFL func coverage")
    func_list_afl = set(func_list_afl)
    print(len(func_list_afl))
    print(func_list_afl)

    uncovered_funcs = []  # all_funcs_topologic - func_list_afl
    for index in range(len(all_funcs_topologic)):
        if all_funcs_topologic[index] not in func_list_afl:
            uncovered_funcs.append(all_funcs_topologic[index])

    print(len(uncovered_funcs))
    print(uncovered_funcs)

    func_dir = OrderedDict()
    for index in range(len(uncovered_funcs)):
        func = uncovered_funcs[index]
        func_dir[func] = 0

    covered_from_klee = set()
    pos = LLVM_OBJECT.rfind('/')
    klee_cov_funcs = LLVM_OBJECT[:pos + 1] + "covered_funcs.txt"
    klee_uncov_funcs = LLVM_OBJECT[:pos + 1] + "uncovered_funcs.txt"
    frontier_nodes = LLVM_OBJECT[:pos + 1] + "frontier_nodes.txt"

    cov_file = open(klee_cov_funcs, "w+")
    uncov_file = open(klee_uncov_funcs, "w+")
    frontier_file = open(frontier_nodes, "w+")

    targ = TARGET_INFO

    # run selected version of KLEE
    for key in func_dir:
        if func_dir[key] != 1:
            print(key)
            args = [os.environ['HOME'] + "/build/klee/Release+Asserts/bin/klee", "--posix-runtime", "--libc=uclibc",
                    "--only-output-states-covering-new",
                    "--disable-inlining", "-output-dir=" + LLVM_OBJECT[:pos + 1] + "/klee-out-" + key, "--optimize", "--max-time=" + FUNC_TIME, "--watchdog",
                    "-search=" + SEARCH_NAME, TARGET_INFO + key, LLVM_OBJECT, SYM_ARGS, SYM_FILES,
                    SYM_STDIN]
            try:
                str_args = " ".join(args)
                print(str_args)
                os.system(str_args)
                #proc = subprocess.run(args, timeout=1680)
            except subprocess.TimeoutExpired:
                print("Exit status of the child process: ", proc.returncode)
                print("Args of the child process: ", proc.args)
                raise

            run_istats = LLVM_OBJECT[:pos + 1] + "klee-out-" + key + "/run.istats"
            covered_from_key = run_klee_cov(LLVM_OBJECT, run_istats)
            
            frontier_file.write("%s:\n" % (key))
            for c in covered_from_key:
                if c in func_dir.keys():
                    if func_dir[c] != 1:
                        func_dir[c] = 1
                        frontier_file.write("\t%s\n" % (c))

    for key in func_dir:
        if func_dir[key] == 1:
            cov_file.write("%s\n" % key)
        else:
            uncov_file.write("%s\n" % key)

    cov_file.close()
    uncov_file.close()
    frontier_file.close()

    return 0


if __name__ == '__main__':
    try:
        config_file = sys.argv[1]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    main(config_file)
