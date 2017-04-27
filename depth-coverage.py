# from covgraph import calc_distance_to_main
import argparse
import json
from glob import glob
from os import path
from pprint import pprint
import subprocess
from itertools import cycle

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
    else:
        klee_file = open(kleecovered_f, 'r')
    if not aflcovered_f:
        afl_file = None
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
    parser = argparse.ArgumentParser(
        description="Calculate call-graph depth-wise"
                    "function coverage"
    )
    parser.add_argument(
        "bitcode",
        help="bitcode file compiled for KLEE")
    parser.add_argument(
        "llvmopt",
        help="The llvm opt binary to be used")
    parser.add_argument(
        "libmackeopt",
        help="Macke optllvm shared library for aggregation functions")
    parser.add_argument(
        "outputtxt",
        help="Write the output to this file")
    parser.add_argument(
        "kleecovered",
        help="textfile listing all covered functions by KLEE")
    parser.add_argument(
        "aflcovered",
        help="textfile listing all covered functions AFL")

    args = parser.parse_args()

    if not args.bitcode.endswith(".bc"):
        print("ERROR: KLEE compiled file should have a .bc extension")
    if not path.isfile(args.llvmopt):
        print("ERROR: llvmopt loader not found: %s"%args.llvmopt)
    if not path.isfile(args.libmackeopt):
        print("ERROR: Macke optllvm library not found: %s"%args.libmackeopt)
    if not args.outputtxt.endswith(".txt"):
        print("ERROR: Output textfile should have .txt extension: %s"%args.outputtxt)
        output_to_file = False
    elif not path.isdir(path.dirname(args.outputtxt)):
        print("ERROR: Output textfile path does not exist: %s"%args.outputtxt)
        output_to_file = False
    else:
        output_to_file = True
    if not (path.isfile(args.kleecovered) or args.kleecovered=="None"):
        print("ERROR: wrong KLEE coverage file - covered: %s"%args.kleecovered)
    if not (path.isfile(args.aflcovered)or args.aflcovered=="None"):
        print("ERROR: wrong AFL coverage file - covered: %s"%args.aflcovered)

    callgraph = json.loads(subprocess.check_output([
                        args.llvmopt, "-load", args.libmackeopt,
                        "-extractcallgraph", args.bitcode,
                        "-disable-output"]).decode("utf-8"))
    all_funcs, distancedict = calc_distance_to_main(callgraph)

    print("Total functions discovered in connected graph: %d"%(len(all_funcs)))
    if args.kleecovered=="None":
        kleecovered_f = None
    else:
        kleecovered_f = args.kleecovered
    if args.aflcovered=="None":
        aflcovered_f = None
    else:
        aflcovered_f = args.aflcovered

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
        outfile = open(args.outputtxt, "w+")
        pprint(depthdict, outfile)

if __name__=='__main__':
    main()
