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


if __name__ == "__main__":
    pipeline = Pipeline()


    @pipeline.task(depends_on=None)
    def first_task(x):
        return x + 1


    @pipeline.task(depends_on=first_task)
    def second_task(x):
        return x * 2


    @pipeline.task(depends_on=second_task)
    def last_task(x):
        return x - 4


    print(pipeline.tasks)
    print(pipeline.run(20))
