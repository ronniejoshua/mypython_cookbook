import csv
import itertools
import datetime as dt


# $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"

def parse_time(time_str):
    """
    Parses time in the format [30/Nov/2017:11:59:54 +0000]
    to a datetime object.
    """
    time_obj = dt.datetime.strptime(time_str, "[%d/%b/%Y:%H:%M:%S %z]")
    return time_obj


def strip_quotes(s):
    return s.replace('"', "")


def parse_log(log):
    for line in log:
        split_line = line.split()
        remote_addr = split_line[0]
        time_local = parse_time(split_line[3] + " " + split_line[4])
        request_type = strip_quotes(split_line[5])
        request_path = split_line[6]
        status = int(split_line[8])
        body_bytes_sent = int(split_line[9])
        http_referrer = strip_quotes(split_line[10])
        http_user_agent = strip_quotes(" ".join(split_line[11:]))
        yield (
            remote_addr,
            time_local,
            request_type,
            request_path,
            status,
            body_bytes_sent,
            http_referrer,
            http_user_agent,
        )


def build_csv(lines, header=None, file=None):
    # If headers are provided then chain the headers and lines
    if header:
        lines = itertools.chain([header], lines)
    writer = csv.writer(file, delimiter=",")
    writer.writerows(lines)
    file.seek(0)
    return file


def count_unique_request_dict(csv_file):
    reader = csv.reader(csv_file)
    header = next(reader)
    idx = header.index("request_type")

    _uniques = {}
    for line in reader:
        if not _uniques.get(line[idx]):
            _uniques[line[idx]] = 0
        _uniques[line[idx]] += 1
    return _uniques


def count_unique_request_tuple(csv_file):
    reader = csv.reader(csv_file)
    header = next(reader)
    idx = header.index("request_type")

    _uniques = {}
    for line in reader:

        if not _uniques.get(line[idx]):
            _uniques[line[idx]] = 0
        _uniques[line[idx]] += 1
    return ((k, v) for k, v in _uniques.items())


if __name__ == "__main__":
    with open("example_log.txt", "r") as log:
        first_line = next(parse_log(log))
        print(first_line)

    with open("example_log.txt", "r") as log:
        parsed = parse_log(log)
        with open("temporary.csv", "w+") as temp_log:
            csv_file = build_csv(
                parsed,
                header=[
                    "ip",
                    "time_local",
                    "request_type",
                    "request_path",
                    "status",
                    "bytes_sent",
                    "http_referrer",
                    "http_user_agent",
                ],
                file=temp_log,
            )

            uniques = count_unique_request_tuple(csv_file)

            with open("summarized.csv", "w+") as summary_log:
                summarized_csv = build_csv(
                    uniques,
                    header=["request_type", "count"],
                    file=summary_log
                )

                print(summarized_csv.readlines())
