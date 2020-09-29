#! /usr/bin/env python3
import argparse
import sys


def fibonacci(n: int) -> int:
    a, b = 0, 1
    assert n >= 0
    for i in range(n):
        a, b = b, a + b
    return a


def main():
    # Method 1
    if len(sys.argv) > 1:
        print("~ sys.argv: ", sys.argv)
        print("~ Script: " + sys.argv[0])
        print("~ Arg : " + sys.argv[1])
    else:
        print(" No arguments ")

    # Method 2
    # https://docs.python.org/3/library/argparse.html#argumentparser-objects
    parser = argparse.ArgumentParser(
        prog="argument_parser.py",
        description='Process some integers.',
        epilog='Enjoy the program! :)',
        prefix_chars='-',
        fromfile_prefix_chars='@',
        allow_abbrev=True,
        add_help=True

    )

    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    # https://mkaz.blog/code/python-argparse-cookbook/
    # Optional Arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose flag')
    parser.add_argument('-l', '--limit', required=True, default=5, type=int)
    parser.add_argument('-s', '--sum', nargs=2)
    parser.add_argument('-m', '--mode', default="closed", choices=['closed', 'wontfix', 'notabug'], help="bug status")
    parser.add_argument('-a', '--act', action='store', type=int, choices=range(1, 5), default=3)
    parser.add_argument('-k', action='store', choices=['head', 'tail'], required=True)
    parser.add_argument('-q', '--verbosity', action='store', type=int, metavar='LEVEL')
    parser.add_argument('-p', '--verbosity-level', action='store', type=int)

    # Positional Arguments
    parser.add_argument('filename', nargs=1, type=argparse.FileType('r'))
    parser.add_argument('n_one', nargs=2, type=int)
    parser.add_argument('n_two', nargs='*', type=int)
    parser.add_argument('n_three', nargs='+', type=int)
    parser.add_argument('n_four', nargs='?')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    parser.add_argument('Path', metavar='_path', type=str, help='the path to list')

    # https://docs.python.org/3/library/argparse.html#the-parse-args-method
    args = parser.parse_args()
    print(f"~ Arguments: {args}")
    print(vars(args))


if __name__ == "__main__":
    main()
