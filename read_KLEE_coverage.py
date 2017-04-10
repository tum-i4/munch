from os.path import expanduser
from helper import order_funcs_topologic
import argparse
import os
import subprocess, time
import glob

MYOPT = expanduser("~/build/llvm/Release/bin/opt")
MYLIBMACKEOPT = expanduser("~/git/macke-opt-llvm/bin/libMackeOpt.so")


def main(bcfilename):
    # get a list of functions topologically ordered
    args = [MYOPT, "-load", MYLIBMACKEOPT, bcfilename,
            "--listallfuncstopologic", "-disable-output"]
    result = subprocess.check_output(args)
    result = str(result, 'utf-8')
    all_funcs_topologic = order_funcs_topologic(result)
    print(all_funcs_topologic)
    print("TOTAL FUNCS : ")
    print(len(all_funcs_topologic))
    time.sleep(5)

    covered_from_klee = set()
    pos = bcfilename.rfind('/')
    klee_cov_funcs = bcfilename[:pos + 1] + "covered_funcs.txt"
    klee_uncov_funcs = bcfilename[:pos + 1] + "uncovered_funcs.txt"

    for filename in glob.glob(bcfilename[:pos + 1] + "klee-out-*"):
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
    parser = argparse.ArgumentParser(
        description="""\
        Extract the achived line coverage from past KLEE runs.
        """
    )
    parser.add_argument(
        'bcfile',
        metavar=".bc-file",
        type=argparse.FileType('r'),
        help="Bitcode file, that was analyzed with KLEE"
    )

    args = parser.parse_args()

    main(args.bcfile.name)

