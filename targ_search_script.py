import os, sys
import subprocess, time, signal
from collections import OrderedDict

def run_afl_cov(prog, path_to_afl_results, code_dir):
    afl_out_res = path_to_afl_results
    output = afl_out_res + "/" + "afl_cov.txt"
    command = "./" + code_dir + " < AFL_FILE"
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
    try:
        afl_binary = sys.argv[1]  # name of the program for afl
        llvm_obj = sys.argv[2]  # name of the program for klee
        testcases = sys.argv[3]  # testcases for the program used by afl-fuzz
        fuzz_time = int(sys.argv[4])  # time to run afl-fuzzer
        gcov_dir = sys.argv[5] # gcov
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise 

    # get a list of functions topologically ordered
    args = ["/home/saahil/build/llvm/Release/bin/opt", "-load", "/home/saahil/git/macke-opt-llvm/bin/libMackeOpt.so", llvm_obj,
            "--listallfuncstopologic", "-disable-output"]
    result = subprocess.check_output(args)
    all_funcs_topologic = order_funcs_topologic(result)
    print("TOTAL FUNCS : ")
    print(len(all_funcs_topologic))

    # run afl-fuzz
    pos = afl_binary.rfind('/')
    afl_out_dir=afl_binary[:pos+1]+"afl_results"
    args = ["afl-fuzz", "-i", testcases, "-o", afl_out_dir, afl_binary]
    # take the progs args as given from command line
    # if sys.argv[5:]:
    #    args = args + sys.argv[5:]

    proc = subprocess.Popen(args)

    time.sleep(fuzz_time)
    os.kill(proc.pid, signal.SIGKILL)

    func_list_afl = run_afl_cov(afl_binary, afl_out_dir, gcov_dir)
    print(len(func_list_afl))
    print(func_list_afl)

    # run KLEE with targeted search with the functions not covered by afl
    # be sure it's topologically sorted
    uncovered_funcs = []
    for index in range(len(all_funcs_topologic)):
        if all_funcs_topologic[index] not in func_list_afl:
            uncovered_funcs.append(all_funcs_topologic[index])

    # save the list of covered and uncovered functions after fuzzing
    cov_funcs = afl_out_dir + "/covered_functions.txt"
    with open(cov_funcs, 'w+') as the_file:
	the_file.write("%s\n" %len(func_list_afl))
	for index in range(len(func_list_afl)):
	    the_file.write("%s\n" %func_list_afl[index])

    uncov_funcs = afl_out_dir + "/uncovered_functions.txt"
    with open(uncov_funcs, 'w+') as the_file:
	the_file.write("%s\n" %len(uncovered_funcs))
        for index in range(len(uncovered_funcs)):
    	    the_file.write("%s\n" %uncovered_funcs[index])
    
    targ = "-targeted-function="
    func_dir = OrderedDict()
    for index in range(len(uncovered_funcs)):
	func = uncovered_funcs[index]
        func_dir[func] = 0

    print(func_dir)
    covered_from_klee = set()
    pos = llvm_obj.rfind('/')
    klee_cov_funcs = llvm_obj[:pos+1] + "covered_funcs.txt"
    klee_uncov_funcs = llvm_obj[:pos+1] + "uncovered_funcs.txt"
  
     
    uncov_file = open(klee_uncov_funcs, 'w+')
    for key in func_dir:
	uncov_file.write("%s\n" %func)
    uncov_file.close()

    for key in func_dir:
	print(key)
        if func_dir[key] != 1:
	    args = ["/home/saahil/repos/klee/Release+Asserts/bin/klee", "--posix-runtime", "--libc=uclibc", "--only-output-states-covering-new", "--disable-inlining", "--optimize", "--max-time=120", "-search=ld2t", targ+key, llvm_obj, "--sym-arg 20", "--sym-stdin 100"]
	    subprocess.Popen(args)
            time.sleep(130)
	    klee_dir=llvm_obj[:pos+1]+"klee-last/run.istats"
	    f = open(klee_dir, "r")

          #  covered_from_klee = set()
            for line in f:
                if line[:4] == "cfn=":
                    covered_from_klee.add(line[4:-1])

	    print("covered_from_klee:")
            print(covered_from_klee)
	    cov_file = open(klee_cov_funcs, 'w+')
#	    uncov_file = open(klee_uncov_funcs, 'w+')
	    for func in covered_from_klee:
                if func in func_dir:
                    func_dir[func] = 1
		    cov_file.write("%s\n" %func)
#		else:
#		    uncov_file.write("%s\n" %func)
	    cov_file.close()
            print(func_dir)

    return 1

if __name__ == '__main__':
    main(sys.argv[1:])

