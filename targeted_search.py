#!/usr/bin/env python3

import os, sys
import subprocess, time, signal
import re

def run_afl_cov(prog, path_to_afl_results):

    # compile program with gcov, in order to run afl_cov
    afl_out_res = "../" + path_to_afl_results
    gcov_dir = prog[:-2] + "_gcov_dir"
    if not os.path.exists(gcov_dir):
        os.makedirs(gcov_dir)
    os.chdir(gcov_dir) # handle exception
    src_file = "../" + prog
    bin_file = prog[:-2]
    args = ["gcc", "-fprofile-arcs", "-ftest-coverage", src_file, "-o", bin_file]
    subprocess.call(args)
    code_dir = "." # gcov_dir
    output = afl_out_res + "/" + prog[:-2] + "_cov.txt"
    command = "./" + bin_file + " < AFL_FILE"
    args = ["afl-cov", "-d", afl_out_res, "-e", command, "-c", code_dir, "--coverage-include-lines", "--src-file", src_file, "-O"]
    file_to_write = open(output, "w+")
    print(args)
    subprocess.call(args, stdout=file_to_write)
    file_to_write.close()

    # get function coverage
    cov_dir = afl_out_res + "/cov/"
    filename = cov_dir + "id-delta-cov"
    f_cov = open(filename, "r")
    next(f_cov)

    write_func = cov_dir + prog[:-2] + "_func_cov.txt"
    f = open(write_func, "a+")

    func_list = []
    for line in f_cov:
        words = line.split(" ")
        if "function" in words[3]:
            func_list.append(words[4][:-3])
            f.write(words[4][:-3] + "\n")

    f.close()
    f_cov.close()

    return func_list


def order_funcs_topologic(list_of_functions):
    func=""
    l = []
    for c in list_of_functions:
        if c not in "[],\n\"":
            if (c==' ') and (func != ""):
                l.append(func)
                func = ""
            else:
                if c != ' ':
                    func += c
    if func != "":
        l.append(func)

    l.reverse()
    print(l)
    return l


def main(argv):

    try:
        prog = sys.argv[1]    # name of the program for afl
        prog_klee = sys.argv[2] # name of the program for klee
        testcases = sys.argv[3] # testcases for the program used by afl-fuzz
        fuzz_time = int(sys.argv[4]) # time to run afl-fuzzer
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # compile twice with afl-clang
    os.environ["AFL_DONT_OPTIMIZE"] = "1"
    llvm_obj = prog_klee[:-2] + ".bc"
    args = ["afl-clang", "-emit-llvm", "-c", "-g", prog_klee, "-o", llvm_obj]
    subprocess.call(args) # creates <prog_name>.bc
    afl_binary = prog[:-2] + " _bin"
    args = ["afl-clang", prog, "-o", afl_binary] # creates the instrumented binary to fuzz with afl
    subprocess.call(args)

    # get a list of functions topologically ordered
    # TODO: Document macke-opt-llvm functions
    args = ["opt-3.4", "-load", "/home/eirini/macke/macke-opt-llvm/bin/libMackeOpt.so", llvm_obj, "--listallfuncstopologic", "-disable-output"]
    result = subprocess.check_output(args)
    all_funcs_topologic = order_funcs_topologic(result)

    # run afl-fuzz
    afl_out_dir = prog[:-2] + "_afl_out_dir"
    afl_binary = "./" + afl_binary
    args = ["afl-fuzz", "-i", testcases, "-o", afl_out_dir, afl_binary]
    # take the progs args as given from command line
    if sys.argv[5:]:
        args = args + sys.argv[5:]

    proc = subprocess.Popen(args)

    time.sleep(fuzz_time)
    os.kill(proc.pid, signal.SIGKILL)

    func_list_afl = run_afl_cov(prog, afl_out_dir)
    print(func_list_afl)

    # run KLEE with targeted search with the functions not covered by afl
    # be sure it's topologically sorted
    uncovered_funcs = []
    for elem in all_funcs_topologic:
        if elem not in func_list_afl:
            uncovered_funcs.append(elem)

    # print(uncovered_funcs)
    uncovered_funcs = ['matchhere']
    os.chdir("../")
    targ = "-targeted-function="   
    # while loop: while there are uncovered functions
    # remove also the functions that covered during this klee run
    while(uncovered_funcs):
        temp = uncovered_funcs
        elem = temp.pop(0)
        args = ["/home/eirini/repos/klee/Release+Asserts/bin/klee", "--disable-inlining", "-search=ld2t", targ+elem, llvm_obj]
        subprocess.call(args)
        # check which funcs are covered and remove them
        f = open("klee-last/run.istats", "r")
       
        covered_from_klee = set()
        for line in f:
            if line[:4] == "cfn=":
                covered_from_klee.add(line[4:-1])

        covered_from_klee = list(covered_from_klee)
        print(covered_from_klee)
        for l in covered_from_klee:
            if l in temp:
                temp.remove(l)      
        uncovered_funcs = temp
        print(uncovered_funcs)

    return 1

if __name__ == '__main__':
    main(sys.argv[1:])

