import os, sys
import subprocess, time, signal
import json
# from collections import OrderedDict

AFL_BINARY = ""
LLVM_OBJ = ""
TESTCASES = ""
FUZZ_TIME = ""
GCOV_DIR = ""
LLVM_OPT = ""
LIB_MACKEOPT = ""
AFL_OUT = ""
AFL_BINARY_ARGS = ""
READ_FROM_FILE = ""
AFL_RESULTS_FOLDER = ""

def read_config(config_file):
    json_file = open(config_file, "r")
    conf = json.load(json_file)

    global AFL_BINARY, LLVM_OBJ, GCOV_DIR, LLVM_OPT, LIB_MACKEOPT, AFL_BINARY_ARGS, AFL_RESULTS_FOLDER
    AFL_BINARY = conf["AFL_BINARY"]
    LLVM_OBJ = conf["LLVM_OBJ"]
    GCOV_DIR = conf["GCOV_DIR"]
    LLVM_OPT = conf["LLVM_OPT"]
    LIB_MACKEOPT = conf["LIB_MACKEOPT"]
    AFL_BINARY_ARGS = conf["AFL_BINARY_ARGS"]
    READ_FROM_FILE = ""
    AFL_RESULTS_FOLDER = conf["AFL_RESULTS_FOLDER"]

def run_afl_cov(prog, path_to_afl_results, code_dir):
    afl_out_res = path_to_afl_results
    output = afl_out_res + "/" + "afl_cov.txt"
    command = '"./' + code_dir + READ_FROM_FILE + ' AFL_FILE"'
    print(command)
    pos = code_dir.rfind('/')
    code_dir = code_dir[:pos+1]
    args = ["afl-cov", "-d", afl_out_res, "-e", command, "-c", code_dir, "--coverage-include-lines", "-O"]
    print(args)
    subprocess.call(args)

    # get function coverage
    cov_dir = afl_out_res + "/cov/"
    filename = cov_dir + "id-delta-cov"
    f_cov = open(filename, "r")
    next(f_cov)

    write_func = cov_dir  + "afl_func_cov.txt"
    f = open(write_func, "w+")

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
    func = ""
    l = []
    for c in list_of_functions:
        if c not in "[],\n\"":
            if (c == ' ') and (func != ""):
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
    global TESTCASES, FUZZ_TIME, AFL_OUT
    try:
        config_file = sys.argv[1]
        TESTCASES = sys.argv[2]  # testcases for the program used by afl-fuzz
        FUZZ_TIME = int(sys.argv[3])  # time to run afl-fuzzer
        # AFL_OUT = sys.argv[4]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    read_config(config_file)
    # get a list of functions topologically ordered
    args = [LLVM_OPT, "-load", LIB_MACKEOPT, LLVM_OBJ,
            "--listallfuncstopologic", "-disable-output"]
    result = subprocess.check_output(args)
    result = str(result, 'utf-8')
    all_funcs_topologic = order_funcs_topologic(result)
    print("TOTAL FUNCS : ")
    print(len(all_funcs_topologic))
    time.sleep(5)

    # run afl-fuzz
    pos = AFL_BINARY.rfind('/')
    AFL_OUT=AFL_BINARY[:pos+1]+AFL_RESULTS_FOLDER
    if not os.path.isdir(AFL_OUT):
        args = ["afl-fuzz", "-i", TESTCASES, "-o", AFL_OUT, AFL_BINARY, AFL_BINARY_ARGS]
        # take the progs args as given from command line
        # if sys.argv[5:]:
        #    args = args + sys.argv[5:]

        print("Preparing to fuzz...")
        time.sleep(3)
        proc = subprocess.Popen(args)

        time.sleep(FUZZ_TIME)
        os.kill(proc.pid, signal.SIGKILL)
    else:
        print("That directory already contains past fuzzing results.")
        print("Continuing with coverage calculation...")
        time.sleep(3)
    
    func_list_afl = run_afl_cov(AFL_BINARY, AFL_OUT, GCOV_DIR)
    print("AFL LIST: ")
    print(len(func_list_afl))
    print(func_list_afl)

    # run KLEE with targeted search with the functions not covered by afl
    # be sure it's topologically sorted
    print("Computing function coverage after fuzzing...")
    time.sleep(3)
    uncovered_funcs = []
    for index in range(len(all_funcs_topologic)):
        if all_funcs_topologic[index] not in func_list_afl:
            uncovered_funcs.append(all_funcs_topologic[index])

    print("UNCOVERED LIST: ")
    print(len(uncovered_funcs))
    print(uncovered_funcs)

    # save the list of covered and uncovered functions after fuzzing
    cov_funcs = AFL_OUT + "/covered_functions.txt"
    with open(cov_funcs, 'w+') as the_file:
        the_file.write("%s\n" %len(func_list_afl))
        for index in range(len(func_list_afl)):
            the_file.write("%s\n" %func_list_afl[index])

    uncov_funcs = AFL_OUT + "/uncovered_functions.txt"
    with open(uncov_funcs, 'w+') as the_file:
        the_file.write("%s\n" %len(uncovered_funcs))
        for index in range(len(uncovered_funcs)):
            the_file.write("%s\n" %uncovered_funcs[index])


    return 1


if __name__ == '__main__':
    main(sys.argv[1:])
