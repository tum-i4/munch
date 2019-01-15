import argparse
import klee_after_search
import fuzz_with_afl

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python fs.py', description='Munch FS mode')
    parser.add_argument('-c', '--config', required=True, help='Path to the configuration file')

    args = parser.parse_args()

    fuzz_with_afl(args.config)
    klee_after_search.main(args.config)
