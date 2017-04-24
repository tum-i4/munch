import os, sys
import subprocess, time
from collections import OrderedDict

sys.path.append("/home/saahil/vdc")
import helper
import argparse
from os import path

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

def main(argv):
    try:
        afl_binary = sys.argv[1]
        llvm_obj = sys.argv[2]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # get a list of functions topologically ordered
    all_funcs_topologic = helper.get_all_called_funcs(llvm_obj)
    print(len(all_funcs_topologic))
    print("All functions:", all_funcs_topologic)

    pos = afl_binary.rfind('/')
    afl_out_dir = afl_binary[:pos + 1] + "afl_results_1h"
    func_list_afl = run_afl_cov(afl_binary, afl_out_dir)
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
    pos = llvm_obj.rfind('/')
    klee_cov_funcs = llvm_obj[:pos + 1] + "covered_funcs.txt"
    klee_uncov_funcs = llvm_obj[:pos + 1] + "uncovered_funcs.txt"
    frontier_nodes = llvm_obj[:pos + 1] + "frontier_nodes.txt"

    cov_file = open(klee_cov_funcs, "w+")
    uncov_file = open(klee_uncov_funcs, "w+")
    frontier_file = open(frontier_nodes, "w+")

    # run KLEE after-search 1.3
    for key in func_dir:
        if func_dir[key] != 1:
            print(key)
            args = ["/home/saahil/repos/after-search/Release+Asserts/bin/klee", "--posix-runtime", "--libc=uclibc",
                    "--only-output-states-covering-new",
                    "--disable-inlining", "-output-dir=" + llvm_obj[:pos + 1] + "/klee-out-"+key, "--optimize", "--max-time=300", "--max-solver-time=15", "--watchdog",
                    "-search=after-call", "--after-function="+key, llvm_obj, "--sym-args 1 3 50", "--sym-files 1 100",
                    "--sym-stdin 100"]
            try:
                str_args = " ".join(args)
                print(str_args)
                os.system(str_args)
                #proc = subprocess.run(args, timeout=1680)
            except subprocess.TimeoutExpired:
                print("Exit status of the child process: ", proc.returncode)
                print("Args of the child process: ", proc.args)
                raise

            run_istats = llvm_obj[:pos + 1] + "klee-out-"+key+"/run.istats"
            covered_from_key = run_klee_cov(llvm_obj, run_istats)
            
            frontier_file.write("%s:\n"%(key))
            for c in covered_from_key:
                if c in func_dir.keys():
                    if func_dir[c] != 1:
                        func_dir[c] = 1
                        frontier_file.write("\t%s\n"%(c))

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
    main(sys.argv[1:])

