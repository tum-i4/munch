import os, sys
import subprocess, time
import glob

def main(argv):
    print(argv)
    try:
        klee_coverage_path = argv[0]
        afl_coverage_path = argv[1]
        after_search_coverage_path = argv[2]
        all_funcs_file = argv[3]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # set of KLEE functions
    if os.path.isfile(klee_coverage_path):
        klee_cov_file = open(klee_coverage_path, "r")
        klee_set = set()
    else:
        print("KLEE coverage file does not exist: %s"%(klee_coverage_path))
        sys.exit(1)

    # set of AFL functions
    if os.path.isfile(afl_coverage_path):
        afl_cov_file = open(afl_coverage_path, "r")
        afl_set = set()
    else:
        print("AFL coverage file does not exist: %s"%(afl_coverage_path))
        sys.exit(1)
    
    # set of Hybrid functions
    if os.path.isfile(after_search_coverage_path):
        after_search_cov_file = open(after_search_coverage_path, "r")
        hybrid_set = set()
    else:
        print("After search coverage file does not exist: %s"%(afl_coverage_path))
        sys.exit(1)

    # set of all functions
    if os.path.isfile(all_funcs_file):
        all_funcs = open(all_funcs_file)
        all_funcs_set = set()
    else:
        print("File with all-functions list does not exist: %s"%(all_funcs_file))
        sys.exit(1)

    for line in all_funcs:
        all_funcs_set.add(line.strip())

    for line in afl_cov_file:
        try:
            line = float(line.strip())
        except:
            afl_set.add(line.strip())
            hybrid_set.add(line.strip())

    afl_set = afl_set.intersection(all_funcs_set)
    hybrid_set = hybrid_set.intersection(all_funcs_set)

    for line in klee_cov_file:
        klee_set.add(line.strip())

    klee_set = klee_set.intersection(all_funcs_set)

    after_set = set()
    for line in after_search_cov_file:
        after_set.add(line.strip())
    after_set = after_set.intersection(all_funcs_set)
    hybrid_set = hybrid_set.union(after_set)

    # Intersections
    klee_afl_intersect = afl_set.intersection(klee_set)
    klee_hybrid_intersect = klee_set.intersection(hybrid_set)
    afl_hybrid_intersect = hybrid_set.intersection(afl_set)
    
    # Unique functions
    klee_only = klee_set.difference(hybrid_set) # klee_set - hybrid_set
    afl_only = afl_set.difference(klee_set) # afl_set - klee_set
    hybrid_only = hybrid_set.difference(klee_set.union(afl_set)) # hybrid_set - (klee_set + afl_set)

    print("AFL coverage: %d"%(len(afl_set)))
    print("KLEE coverage: %d"%(len(klee_set)))
    print("Hybrid coverage: %d"%(len(hybrid_set)))

    print("\n")
    print("KLEE+AFL: %d"%(len(klee_afl_intersect)))
    print("AFL+Hybrid: %d"%(len(afl_hybrid_intersect)))
    print("KLEE+Hybrid: %d"%(len(klee_hybrid_intersect)))

    print("\n")
    print("AFL only: %d"%(len(afl_only)))
    print("KLEE only: %d"%(len(klee_only)))
    print("Hybrid only: %d"%(len(hybrid_only)))

if __name__ == '__main__':
    main(sys.argv[1:])

