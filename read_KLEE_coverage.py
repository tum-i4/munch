from helper import get_flat_inversed_topology
import argparse
from os import path
import time
from glob import glob


def main(bcfilename, verbose=False):
    # get a list of functions topologically ordered
    all_funcs_topologic = list(get_flat_inversed_topology(bcfilename))
    if verbose:
        print("All functions:", all_funcs_topologic)

    covered_from_klee = set()
    for filename in glob(path.join(path.dirname(bcfilename), "klee-out-*")):
        runistatsfile = path.join(path.abspath(filename), "run.istats")
        print(runistatsfile)
        f = open(runistatsfile, "r")
        for line in f:
            if line[:4] == "cfn=":
                covered_from_klee.add(line[4:-1])

    if verbose:
        print(covered_from_klee)

    print("KLEE covers {:d} out of {:d} total functions ({:.1%})".format(
        len(covered_from_klee), len(all_funcs_topologic),
        len(covered_from_klee) / len(all_funcs_topologic)))

    klee_cov_funcs = path.join(path.dirname(bcfilename), "covered_funcs.txt")
    klee_unc_funcs = path.join(path.dirname(bcfilename), "uncovered_funcs.txt")

    cov_file = open(klee_cov_funcs, 'w+')
    unc_file = open(klee_unc_funcs, 'w+')
    for func in all_funcs_topologic:
        if func in covered_from_klee:
            cov_file.write("%s\n" % func)
        else:
            unc_file.write("%s\n" % func)

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
    parser.add_argument(
        "-v", "--verbose",
        help="Increase output verbosity",
        action="store_true"
    )

    args = parser.parse_args()

    main(args.bcfile.name, args.verbose)

