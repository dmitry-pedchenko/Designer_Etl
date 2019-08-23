import argparse
import sys


class Opts:

    example = """--config must be entered\npython {} --test_mode [true/false] --config [args]"""

    def __init__(self):
        parser = argparse.ArgumentParser(description='Parse args.')
        parser.add_argument('--test_mode', type=str, help='Run test mode.')
        parser.add_argument('--config', type=str, nargs='*')
        self.args = parser.parse_args()

        self.checkArgs()

    def checkArgs(self):
        if len(self.args.config) < 1:
            print(self.example.format(sys.argv[0]))
            raise SystemExit(1)

        if self.args.test_mode is None:
            print(self.example.format(sys.argv[0]))
            raise SystemExit(1)

