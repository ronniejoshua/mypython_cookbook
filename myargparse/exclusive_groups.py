#! /usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-v', '--verbose', action='store_true')
    group.add_argument('-s', '--silent', action='store_true')

    args = parser.parse_args()
    print(f"type(args): {type(args)}")
    print(f"~ Arguments: {vars(args)}")


if __name__ == "__main__":
    main()
