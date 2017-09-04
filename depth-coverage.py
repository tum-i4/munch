# from covgraph import calc_distance_to_main
import argparse
import json
from glob import glob
from os import path
from pprint import pprint
import subprocess
from itertools import cycle
import helper
import essentials as es
import sys
import fuzz_with_afl, read_KLEE_coverage

def calc_distance_to_main(callgraph):
    all_funcs = []
    result = dict(zip(callgraph.keys(), cycle([-1])))

    if "main" not in callgraph:
        return all_funcs, result

    all_funcs.append("main")
    result["main"] = 0

    nextlevel = callgraph["main"]["calls"]
    level = 1
    while nextlevel:
        oldlevel = list(nextlevel)
        nextlevel = []

        for function in oldlevel:
            if callgraph[function]["isexternal"] == True:
                continue
            if result[function] < 0:
                result[function] = level
                all_funcs.append(function)
                nextlevel.extend(callgraph[function]["calls"])

        level += 1

    return all_funcs, result

def read_coverage(kleecovered_f, aflcovered_f):
    if not kleecovered_f:
        klee_file = None
        print("Not reading KLEE coverage.")
    else:
        klee_file = open(kleecovered_f, 'r')
    if not aflcovered_f:
        afl_file = None
        print("Not reading AFL coverage.")
    else:
        afl_file = open(aflcovered_f, 'r')

    covered = []
    if klee_file:
        for line in klee_file:
            if line.strip() not in covered:
                covered.append(line.strip())
    if afl_file:
        for line in afl_file:
            try:
                float(line.strip())
            except:
                if line.strip() not in covered:
                    covered.append(line.strip())

    return covered

def main():
    try:
        config_file = sys.argv[1]
        outputtxt = sys.argv[2]
    except IndexError:
        print("Wrong number of command line ", sys.exc_info()[0])
        raise
    
    helper.read_config(config_file)
    
    bitcode = es.LLVM_OBJ
    llvmopt = es.LLVM_OPT
    libmackeopt = es.LIB_MACKEOPT
    kleecovered = path.dirname(es.LLVM_OBJ)+"/covered_funcs.txt"
    aflcovered = path.dirname(es.AFL_BINARY)+"/"+es.AFL_RESULTS_FOLDER+"/covered_functions.txt"

    if not bitcode.endswith(".bc"):
        print("ERROR: KLEE compiled file should have a .bc extension")
    if not path.isfile(llvmopt):
        print("ERROR: llvmopt loader not found: %s"%llvmopt)
    if not path.isfile(libmackeopt):
        print("ERROR: Macke optllvm library not found: %s"%libmackeopt)
    if not outputtxt.endswith(".txt"):
        print("ERROR: Output textfile should have .txt extension: %s"%outputtxt)
        output_to_file = False
    elif not path.isdir(path.dirname(outputtxt)):
        print("ERROR: Output textfile path does not exist: %s"%outputtxt)
        output_to_file = False
    else:
        output_to_file = True

    if not path.isfile(kleecovered) and kleecovered!="None":
        print("ERROR: wrong KLEE coverage file: %s\nGenerating now..."%kleecovered)
        read_KLEE_coverage.main(bitcode, verbose=False, store=True)
    if not path.isfile(aflcovered) and aflcovered!="None":
        print("ERROR: wrong AFL coverage file: %s\nGenerating now..."%aflcovered)
        fuzz_with_afl.run_afl_cov(es.AFL_BINARY, path.dirname(es.AFL_BINARY)+"/"+es.AFL_RESULTS_FOLDER, es.GCOV_DIR)

    callgraph = json.loads(subprocess.check_output([
                        llvmopt, "-load", libmackeopt,
                        "-extractcallgraph", bitcode,
                        "-disable-output"]).decode("utf-8"))
    all_funcs, distancedict = calc_distance_to_main(callgraph)

    print("Total functions discovered in connected graph: %d"%(len(all_funcs)))
    if kleecovered=="None":
        kleecovered_f = None
    else:
        kleecovered_f = kleecovered
    if aflcovered=="None":
        aflcovered_f = None
    else:
        aflcovered_f = aflcovered

    covered = read_coverage(kleecovered_f, aflcovered_f)

    depthdict = {}
    covered_funcs_connected = []
    for d in distancedict.keys():
        depth = distancedict[d]
        if depth==-1:
            continue
        if depth not in depthdict.keys():
            depthdict[depth] = [[], []]
        if d in covered:
            covered_funcs_connected.append(d)
            if d not in depthdict[depth][0]:
                depthdict[depth][0].append(d)
        else:
            if d not in depthdict[depth][1]:
                depthdict[depth][1].append(d)
    
    print("Total functions covered in connected graph: %d"%(len(covered_funcs_connected)))
    print("Covered   |     Total")
    for d in depthdict.keys():
        print("%10d|%10d"%(len(depthdict[d][0]), len(depthdict[d][0]) + len(depthdict[d][1])))

    if output_to_file:
        outfile = open(outputtxt, "w+")
        pprint(depthdict, outfile)

if __name__=='__main__':
    main()
