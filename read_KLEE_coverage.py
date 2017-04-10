from helper import get_flat_inversed_topology
import argparse
from os import path
from glob import glob


def main(bcfilename, verbose=False):
    # get a list of functions topologically ordered
    all_funcs_topologic = list(get_flat_inversed_topology(bcfilename))
    if verbose:
        print("All functions:", all_funcs_topologic)

    # TODO: This silently assumes that all klee-out-* dirs are in the
    # same folder as the .bc-file. Maybe add an additional argument?
    for filename in glob(path.join(path.dirname(bcfilename), "klee-out-*")):
        runistatsname = path.join(path.abspath(filename), "run.istats")
        print(runistatsname)
        with open(runistatsname) as runistats:
            covered_from_klee = set(
                line[len("cfn="):-1]
                for line in runistats.readlines()
                if line.startswith("cfn=")
            )

    if verbose:
        print(covered_from_klee)

    print("KLEE covers {:d} out of {:d} total functions ({:.1%})".format(
        len(covered_from_klee), len(all_funcs_topologic),
        len(covered_from_klee) / len(all_funcs_topologic)))

    klee_cov_funcs = path.join(path.dirname(bcfilename), "covered_funcs.txt")
    klee_unc_funcs = path.join(path.dirname(bcfilename), "uncovered_funcs.txt")

    # TODO Maybe order both files alphabetically?
    with open(klee_cov_funcs, 'w+') as cov_file, open(klee_unc_funcs, 'w+') as unc_file:
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

