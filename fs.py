import argparse
import klee_after_search
import fuzz_with_afl
from helper import read_config
import essentials as es
import os

global AFL_OBJ, WHICH_KLEE, LLVM_OBJ, TESTCASES, FUZZ_TIME, GCOV_DIR, LLVM_OPT, LIB_MACKEOPT, AFL_BINARY_ARGS, READ_FROM_FILE, OUTPUT_DIR, AFL_RESULTS_FOLDER, KLEE_RESULTS_FOLDER, FUZZ_TIME

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python fs.py', description='Munch FS mode')
    parser.add_argument('-c', '--config', required=True, help='Path to the configuration file')

    args = parser.parse_args()

    read_config(args.config)
    print("Output directory: %s"%(es.OUTPUT_DIR))

    if not os.path.isdir(es.OUTPUT_DIR):
        os.system("mkdir %s"%(es.OUTPUT_DIR))
    fuzz_with_afl.main(args.config)
    klee_after_search.main(args.config)
