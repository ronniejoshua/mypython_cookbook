#! /usr/bin/env python3

import argparse


def main():
    my_parser = argparse.ArgumentParser()
    my_parser.version = '1.0'
    my_parser.add_argument('-a', action='store')
    my_parser.add_argument('-b', action='store_const', const=42)
    my_parser.add_argument('-c', action='store_true')
    my_parser.add_argument('-d', action='store_false')
    my_parser.add_argument('-e', action='append')
    my_parser.add_argument('-f', action='append_const', const=42)
    my_parser.add_argument('-g', action='count')
    my_parser.add_argument('-i', action='help')
    my_parser.add_argument('-j', action='version')

    args = my_parser.parse_args()
    print(f"type(args): {type(args)}")
    print(f"~ Arguments: {args}")
    print(vars(args))


if __name__ == "__main__":
    main()
