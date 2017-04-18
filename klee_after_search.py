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
    afl_out_dir = afl_binary[:pos + 1] + "afl_results"
    func_list_afl = run_afl_cov(afl_binary, afl_out_dir)
    print("AFL func coverage")
    func_list_afl = set(func_list_afl)
    print(len(func_list_afl))
    print(func_list_afl)

    print("Computing function coverage after fuzzing...")
    time.sleep(3)
    uncovered_funcs = [] # all_funcs_topologic - func_list_afl
    for index in range(len(all_funcs_topologic)):
        if all_funcs_topologic[index] not in func_list_afl:
            uncovered_funcs.append(all_funcs_topologic[index])

    print(len(uncovered_funcs))
    print(uncovered_funcs)

    targ = "--after-function="
    func_dir = OrderedDict()
    for index in range(len(uncovered_funcs)):
        func = uncovered_funcs[index]
        func_dir[func] = 0

    covered_from_klee = set()
    pos = llvm_obj.rfind('/')
    klee_cov_funcs = llvm_obj[:pos + 1] + "covered_funcs.txt"
    klee_uncov_funcs = llvm_obj[:pos + 1] + "uncovered_funcs.txt"

    # run KLEE after-search 1.3
    for key in func_dir:
        print(key)
        if func_dir[key] != 1:
            args = ["/home/saahil/repos/after-search/Release+Asserts/bin/klee", "--posix-runtime", "--libc=uclibc","--only-output-states-covering-new", 
		    "--disable-inlining", "--optimize", "--max-time=150", "--watchdog",
                    "-search=after-call", targ+key, llvm_obj, "--sym-args 1 3 50", "--sym-files 1 100"]
            subprocess.run(args, timeout=150)
            klee_dir = llvm_obj[:pos + 1] + "klee-last/run.istats"
            f = open(klee_dir, "r")
            for line in f:
                if line[:4] == "cfn=":
                    covered_from_klee.add(line[4:-1])

            print("covered_from_klee:")
            print(covered_from_klee)
            for func in covered_from_klee:
                if func in func_dir:
                    func_dir[func] = 1

    print(len(covered_from_klee))
    print(covered_from_klee)
    cov_file = open(klee_cov_funcs, 'w+')
    uncov_file = open(klee_uncov_funcs, 'w+')
    for key in func_dir:
        if func_dir[key] == 1:
            cov_file.write("%s\n" %key)
        else:
            uncov_file.write("%s\n" %key)


    cov_file.close()
    uncov_file.close()

    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
