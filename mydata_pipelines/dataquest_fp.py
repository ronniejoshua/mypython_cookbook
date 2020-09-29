from functools import partial, reduce


def read(filename):
    with open(filename, "r") as f:
        return [line for line in f]


def count(lines):
    return len(lines)


def compose(*functions):
    def inner(arg):
        for func in functions:
            print(f"calling {func}")
            arg = func(arg)
        return arg

    return inner


if __name__ == "__main__":
    lines = read("example_log.txt")
    lines_count = count(lines)

    # Sorting the lines in a list based on a key
    sorted_lines = sorted(lines, key=lambda x: x.split(" ")[5])

    # Extracting a list of IP addresses
    # ---------------------------------
    # Using map()
    ip_addresses = list(map(lambda x: x.split()[0], lines))

    # Using list comprehension
    lc_ip_addresses = [line.split()[0] for line in lines]

    # Filtering and returning a list of IP addresses
    # ----------------------------------------------
    # Using filter()
    filtered_ips = list(filter(lambda x: int(x.split(".")[0]) <= 20, ip_addresses))

    # Using List Comprehension
    lc_filtered_ips = [ip.split(".")[0] for ip in ip_addresses if int(ip.split(".")[0]) <= 20]

    # Using the reduce()
    count_all = reduce(lambda x, _: 2 if isinstance(x, str) else x + 1, lines)
    count_filtered = reduce(lambda x, _: 2 if isinstance(x, str) else x + 1, filtered_ips)
    ratio = count_filtered / count_all

    # Example 1
    # `Using Sorted, Map, filter, reduce, partial and lambda functions
    # ---------------------------------------------------------------

    lines = read("example_log.txt")
    sorted_lines = sorted(lines, key=lambda x: x.split(" ")[5])
    ip_addresses = list(map(lambda x: x.split()[0], lines))
    filtered_ips = list(filter(lambda x: int(x.split(".")[0]) <= 20, ip_addresses))

    count_all = count(lines)
    generic_count = partial(reduce, lambda x, _: 2 if isinstance(x, str) else x + 1)
    count_filtered = generic_count(filtered_ips)
    ratio = count_filtered / count_all
    print(ratio)

    # Example 2
    # Using Sorted, Map, filter, reduce, partial, compose and lambda functions
    # ------------------------------------------------------------------------

    lines = read("mini_log.txt")
    extract_ips = partial(map, lambda x: x.split()[0])
    filter_ips = partial(filter, lambda x: int(x.split(".")[0]) <= 20)
    generic_count = partial(reduce, lambda x, _: 2 if isinstance(x, str) else x + 1)

    composed = compose(extract_ips, filter_ips, generic_count)
    counted = composed(lines)
    print(counted)
