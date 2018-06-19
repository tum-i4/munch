import argparse
import klee_after_search


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='python fs.py', description='Munch FS mode')
    parser.add_argument('-c', '--config', required=True, help='Path to the configuration file')

    args = parser.parse_args()

    klee_after_search.main(args.config)
