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
    # https://mkaz.blog/code/python-argparse-cookbook/
    # https://realpython.com/command-line-interfaces-python-argparse/

    # https://docs.python.org/3/library/argparse.html#argumentparser-objects
    parser = argparse.ArgumentParser(
        prog="fibonacci.py",
        description='Calculate the fibonacci of a given number.',
        epilog='Enjoy the program! :)'
    )

    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    # Optional Arguments
    # parser.add_argument('-n', '--verbose', action='store_true', help='verbose flag')

    # Positional Arguments
    parser.add_argument('num', nargs=1, type=int, help='Provide a positive integer')

    # https://docs.python.org/3/library/argparse.html#the-parse-args-method
    args = parser.parse_args()
    print(f"type(args): {type(args)}")
    print(f"~ Arguments: {args}")
    print(vars(args))
    print(f"~ Arguments: {args.num}")
    print(f"type(args.num): {type(args.num)}")


if __name__ == "__main__":
    main()
