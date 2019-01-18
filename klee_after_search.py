import os, sys
import subprocess, time
from collections import OrderedDict
import helper
import argparse
from os import path
import json
from pprint import pprint
from helper import read_config
import essentials as es

SEARCH_NAME = ""
TARGET_INFO = ""
SYM_STDIN = ""
SYM_ARGS = ""
SYM_FILES = ""
KLEE_TIME = ""

global AFL_OBJ, WHICH_KLEE, LLVM_OBJ, TESTCASES, FUZZ_TIME, GCOV_DIR, LLVM_OPT, LIB_MACKEOPT, AFL_BINARY_ARGS, READ_FROM_FILE, OUTPUT_DIR, AFL_RESULTS_FOLDER, KLEE_RESULTS_FOLDER, FUZZ_TIME

#sys.path.append("/home/saahil/vdc")

def print_config():
    print("AFL_OBJECT: %s"%(AFL_OBJ))
    print("LLVM_OBJECT: %s"%(LLVM_OBJ))
    print("WHICH_KLEE: %s"%(WHICH_KLEE))
    print("AFL_FOLDER_NAME: %s"%(AFL_FOLDER_NAME))
    print("SEARCH_NAME: %s"%(SEARCH_NAME))
    print("TARGET_INFO: %s"%(TARGET_INFO))
    print("SYM_STDIN: %s SYM_ARGS: %s SYM_FILES: %s"%(SYM_STDIN, SYM_ARGS, SYM_FILES))
    print("KLEE_TIME: %s"%(KLEE_TIME))

""" Get configuration for after-search """
def read_config_repeat(config_file):
    json_file = open(config_file, "r")
    conf = json.load(json_file)

    global AFL_OBJECT, LLVM_OBJECT, WHICH_KLEE, AFL_FOLDER_NAME, SEARCH_NAME, TARGET_INFO, SYM_STDIN, SYM_ARGS, SYM_FILES, KLEE_TIME
    #AFL_OBJECT = conf['AFL_OBJECT']
    #LLVM_OBJECT = conf["LLVM_OBJECT"]
    #WHICH_KLEE = conf["WHICH_KLEE"]
    #AFL_FOLDER_NAME = conf["AFL_FOLDER_NAME"]
    SEARCH_NAME = conf["SEARCH_NAME"]
    TARGET_INFO = conf["TARGET_INFO"]
    SYM_STDIN = conf["SYM_STDIN"]
    SYM_ARGS = conf["SYM_ARGS"]
    SYM_FILES = conf["SYM_FILES"]
    KLEE_TIME = conf["KLEE_TIME"]

    #print_config()

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
    read_config_repeat(config_file)

    # get a list of functions topologically ordered
    all_funcs_topologic = helper.get_all_called_funcs(es.LLVM_OBJ)
    #print("Found %d functions in the program..."%len(all_funcs_topologic))
    #print("All functions:", all_funcs_topologic)

    afl_out_dir = es.AFL_RESULTS_FOLDER 
    func_list_afl = run_afl_cov(es.AFL_OBJ, afl_out_dir)
    #print("AFL func coverage")
    func_list_afl = set(func_list_afl)
    #print(len(func_list_afl))
    #print(func_list_afl)

    uncovered_funcs = []  # all_funcs_topologic - func_list_afl
    for index in range(len(all_funcs_topologic)):
        if all_funcs_topologic[index] not in func_list_afl:
            uncovered_funcs.append(all_funcs_topologic[index])

    print("Functions to be covered by KLEE: %d"%len(uncovered_funcs))
    #print(uncovered_funcs)

    func_dir = OrderedDict()
    for index in range(len(uncovered_funcs)):
        func = uncovered_funcs[index]
        func_dir[func] = 0

    covered_from_klee = set()
    #pos = LLVM_OBJECT.rfind('/')
    if not os.path.isdir(es.KLEE_RESULTS_FOLDER):
        os.system("mkdir %s"%(es.KLEE_RESULTS_FOLDER))

    klee_cov_funcs = os.path.join(es.KLEE_RESULTS_FOLDER, "covered_funcs.txt")
    klee_uncov_funcs = os.path.join(es.KLEE_RESULTS_FOLDER, "uncovered_funcs.txt")
    frontier_nodes = os.path.join(es.KLEE_RESULTS_FOLDER, "frontier_nodes.txt")

    cov_file = open(klee_cov_funcs, "w+")
    uncov_file = open(klee_uncov_funcs, "w+")
    frontier_file = open(frontier_nodes, "w+")

    targ = TARGET_INFO

    FUNC_TIME = str(int(KLEE_TIME)/len(func_dir.keys()))
    print("KLEE will be run for %s seconds for each function"%(FUNC_TIME))

    # run selected version of KLEE
    for key in func_dir:
        if func_dir[key] != 1:
            print(key)
            args = [es.WHICH_KLEE, "--posix-runtime", "--libc=uclibc",
                    "--only-output-states-covering-new",
                    "--disable-inlining", "-output-dir=" + es.KLEE_RESULTS_FOLDER + "/klee-out-" + key, "--optimize", "--max-time=" + FUNC_TIME, "--watchdog",
                    "-search=" + SEARCH_NAME, TARGET_INFO + key, es.LLVM_OBJ, SYM_ARGS, SYM_FILES,
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

            run_istats = es.KLEE_RESULTS_FOLDER + "/klee-out-" + key + "/run.istats"
            covered_from_key = run_klee_cov(es.LLVM_OBJ, run_istats)
            
            frontier_file.write("%s:\n" % (key))
            for c in covered_from_key:
                if c in func_dir.keys():
                    if func_dir[c] != 1:
                        func_dir[c] = 1
                        frontier_file.write("\t%s\n" % (c))

    covered = 0
    uncovered = 0
    for key in func_dir:
        if func_dir[key] == 1:
            covered += 1
            cov_file.write("%s\n" % key)
        else:
            uncovered += 1
            uncov_file.write("%s\n" % key)

    cov_file.close()
    uncov_file.close()
    frontier_file.close()

    print("%d more functions covered by KLEE."%(covered))
    print("%d functions still uncovered"%(uncovered))
    return 0

if __name__ == '__main__':
    try:
        config_file = sys.argv[1]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    main(config_file)
