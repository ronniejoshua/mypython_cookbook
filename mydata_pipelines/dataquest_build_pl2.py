import itertools
import datetime as dt
import io
import csv


# https://stackoverflow.com/questions/64062075/how-can-one-use-an-instance-method-as-decorator


class Pipeline(object):
    def __init__(self):
        self.tasks = list()

    def task(self, depends_on=None):
        idx = 0
        if depends_on:
            idx = self.tasks.index(depends_on) + 1

        def inner(func):
            self.tasks.insert(idx, func)
            return func

        return inner

    def run(self, intial_input):
        """
        This method should act like functional composition where it takes the
        previous function's output, and inputs it into the following function.
        """
        output = intial_input
        for each_task in self.tasks:
            output = each_task(output)
        return output


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
    if header:
        lines = itertools.chain([header], lines)
    writer = csv.writer(file, delimiter=",")
    writer.writerows(lines)
    file.seek(0)
    return file


def count_unique_request_tuple(csv_file):
    reader = csv.reader(csv_file)
    header = next(reader)
    idx = header.index("request_type")

    uniques = {}
    for line in reader:

        if not uniques.get(line[idx]):
            uniques[line[idx]] = 0
        uniques[line[idx]] += 1
    return ((k, v) for k, v in uniques.items())


if __name__ == "__main__":
    pipeline = Pipeline()

    @pipeline.task(depends_on=None)
    def wrap_parse_log(logs):
        return parse_log(logs)


    @pipeline.task(depends_on=wrap_parse_log)
    def wrap_build_csv(lines):
        return build_csv(
            lines,
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
            file=io.StringIO()
        )


    @pipeline.task(depends_on=wrap_build_csv)
    def wrap_count_unique_request_tuple(csv_file):
        return count_unique_request_tuple(csv_file)


    @pipeline.task(depends_on=wrap_count_unique_request_tuple)
    def summarize_csv(lines):
        return build_csv(lines, header=["request_type", "count"], file=io.StringIO())


    with open("example_log.txt", "r") as log:
        summarized_file = pipeline.run(log)
        print(summarized_file.readlines())
