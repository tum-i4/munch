import os, sys
import subprocess, time
import glob


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
        llvm_obj = sys.argv[1]  # name of the program for klee
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # get a list of functions topologically ordered
    args = ["/home/saahil/build/llvm/Release/bin/opt", "-load", "/home/saahil/git/macke-opt-llvm/bin/libMackeOpt.so",
            llvm_obj,
            "--listallfuncstopologic", "-disable-output"]
    result = subprocess.check_output(args)
    result = unicode(result, 'utf-8')
    all_funcs_topologic = order_funcs_topologic(result)
    print("TOTAL FUNCS : ")
    print(len(all_funcs_topologic))
    time.sleep(5)

    covered_from_klee = set()
    pos = llvm_obj.rfind('/')
    klee_cov_funcs = llvm_obj[:pos + 1] + "covered_funcs.txt"
    klee_uncov_funcs = llvm_obj[:pos + 1] + "uncovered_funcs.txt"

    for filename in glob.glob(llvm_obj[:pos + 1] + "klee-out-*"):
    	klee_dir = os.path.abspath(filename) + "/run.istats"
        print(klee_dir)
        f = open(klee_dir, "r")
        for line in f:
            if line[:4] == "cfn=":
        	covered_from_klee.add(line[4:-1])

    print(len(covered_from_klee))
    print(covered_from_klee)
    cov_file = open(klee_cov_funcs, 'w+')
    uncov_file = open(klee_uncov_funcs, 'w+')
    for func in all_funcs_topologic:
        if func in covered_from_klee:
            cov_file.write("%s\n" % func)
        else:
            uncov_file.write("%s\n" % func)

    return 1


if __name__ == '__main__':
    main(sys.argv[1:])

