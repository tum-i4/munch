import os, sys
import subprocess, time
import glob

def read_coverage_file(coverage_file_path):
    cov = []
    if not os.path.exists(coverage_file_path):
        print("Path does not exist: %s"%(coverage_file_path))
        return []

    cov_file = open(coverage_file_path)
    for line in cov_file:
        try:
            n_cov = float(line.strip())
        except:
            cov.append(line.strip())

    cov.append("main")
    return cov

def main(argv):
    print(argv)
    try:
        klee_coverage_path = argv[1]
        afl_coverage_path = argv[2]
        fs_coverage_path = argv[3]
        sf_coverage_path = argv[4]
        all_funcs_file = argv[5]
    except IndexError:
        print("Wrong number of command line args:", sys.exc_info()[0])
        raise

    # set of KLEE functions
    klee_set = set(read_coverage_file(klee_coverage_path))
    if not klee_set:
        #print("KLEE coverage file does not exist: %s"%(klee_coverage_path))
        sys.exit(1)

    # set of AFL functions
    afl_set = set(read_coverage_file(afl_coverage_path))
    if not afl_set:
        #print("KLEE coverage file does not exist: %s"%(klee_coverage_path))
        sys.exit(1)
    
    # set of FS functions
    fs_set = set(read_coverage_file(fs_coverage_path))
    if not fs_set:
        sys.exit(1)
    
    # set of SF functions
    sf_set = set(read_coverage_file(sf_coverage_path))
    if not sf_set:
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

    afl_set = afl_set.intersection(all_funcs_set)
    fs_set = fs_set.intersection(all_funcs_set)
    sf_set = sf_set.intersection(all_funcs_set)
    klee_set = klee_set.intersection(all_funcs_set)

    # Intersections
    klee_afl_intersect = afl_set.intersection(klee_set)
    klee_fs_intersect = klee_set.intersection(fs_set)
    klee_sf_intersect = klee_set.intersection(sf_set)
    
    afl_fs_intersect = afl_set.intersection(fs_set)
    afl_sf_intersect = afl_set.intersection(sf_set)

    fs_sf_intersect = fs_set.intersection(sf_set)

    klee_afl_fs_intersect = klee_set.intersection(afl_set.intersection(fs_set))
    klee_afl_sf_intersect = klee_set.intersection(afl_set.intersection(sf_set))
    afl_fs_sf_intersect = afl_set.intersection(fs_set.intersection(sf_set))

    all_intersect = klee_set.intersection(afl_set.intersection(sf_set.intersection(fs_set)))
    
    # Unique functions
    #klee_only = klee_set.difference(hybrid_set) # klee_set - hybrid_set
    #afl_only = afl_set.difference(klee_set) # afl_set - klee_set
    #hybrid_only = hybrid_set.difference(klee_set.union(afl_set)) # hybrid_set - (klee_set + afl_set)

    print("AFL coverage: %d"%(len(afl_set)))
    print("KLEE coverage: %d"%(len(klee_set)))
    print("FS coverage: %d"%(len(fs_set)))
    print("SF coverage: %d"%(len(sf_set)))

    print("\n")
    print("KLEE & AFL: %d"%(len(klee_afl_intersect)))
    print("KLEE & FS: %d"%(len(klee_fs_intersect)))
    print("KLEE & SF: %d"%(len(klee_sf_intersect)))
    print("AFL & FS: %d"%(len(afl_fs_intersect)))
    print("AFL & SF: %d"%(len(afl_sf_intersect)))
    print("FS & SF: %d"%(len(fs_sf_intersect)))

    print("\n")
    print("KLEE & AFL & FS: %d"%(len(klee_afl_fs_intersect)))
    print("KLEE & AFL & SF: %d"%(len(klee_afl_sf_intersect)))
    print("AFL & FS & SF: %d"%(len(afl_fs_sf_intersect)))

    print("\n")
    print("All intersect: %d"%(len(all_intersect)))

    """
    print("\n")
    print("AFL only: %d"%(len(afl_only)))
    print("KLEE only: %d"%(len(klee_only)))
    print("Hybrid only: %d"%(len(hybrid_only)))
    """

if __name__ == '__main__':
    main(sys.argv)

