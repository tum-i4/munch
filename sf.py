import argparse
import read_klee_testcases
import fuzz_with_afl


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python sf.py', description='Munch SF mode')
    parser.add_argument('-c', '--config', required=True, help='Path to the configuration file')
    parser.add_argument('-t', '--time', required=True, help='The time (second) for fuzzing')
    parser.add_argument('--klee-out-folder', required=True, help='Path to the folder named klee-out-X')
    parser.add_argument('--testcase-output-folder', required=True, help='Path for storage the testcase for AFL')

    args = parser.parse_args()

    read_klee_testcases.main(args.klee_out_folder, args.testcase_output_folder)
    fuzz_with_afl.main(args.config, args.testcase_output_folder + '/stdin', args.time)
