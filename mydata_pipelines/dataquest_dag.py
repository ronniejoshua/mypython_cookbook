from collections import deque


class DAG(object):
    def __init__(self):
        self.graph = dict()

    def add(self, node, to=None):
        # if not (node in self.graph)
        # if not (False)
        # if true
        if not node in self.graph:
            self.graph[node] = list()

        # to=None=False
        if to:
            # if not (to in self.graph)
            # if not (False)
            # if true
            if not to in self.graph:
                self.graph[to] = list()
            self.graph[node].append(to)

        if len(self.sort()) != len(self.graph):
            raise Exception

    def in_degrees(self):
        """
        {
            'self.degrees': {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 3},
            'self.graph': {1: [2, 3, 4], 2: [6], 3: [5], 4: [7], 5: [7], 6: [7], 7: []}
        }
        """
        self.degrees = dict()

        # If the node is available in self.graph
        for node in self.graph:
            # if the node is not in self.degrees
            if node not in self.degrees:
                self.degrees[node] = 0

            # self.graph[node] returns a list
            for pointed in self.graph[node]:
                # self.degrees is a dict
                # iterates over the keys of the self.degrees dict
                if pointed not in self.degrees:
                    self.degrees[pointed] = 0
                self.degrees[pointed] += 1

    def sort(self):
        """
        {
        'self.degrees': {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 3},
        'self.graph': {1: [2, 3, 4], 2: [6], 3: [5], 4: [7], 5: [7], 6: [7], 7: []}
        }
        """
        self.in_degrees()
        to_visit = deque()
        for node in self.graph:
            # Condition for root node
            if self.degrees[node] == 0:
                to_visit.append(node)

        searched = list()
        while to_visit:
            # Take the first node in the to_vist deque
            node = to_visit.popleft()
            for pointer in self.graph[node]:
                # Reduece the degree to that pointer
                self.degrees[pointer] -= 1

                # if there are 0 in-degree to that node
                if self.degrees[pointer] == 0:
                    to_visit.append(pointer)
            searched.append(node)
        return searched


class Pipeline(object):
    def __init__(self):
        self.tasks = DAG()

    def task(self, depends_on=None):
        def inner(f):
            self.tasks.add(f)
            if depends_on:
                self.tasks.add(depends_on, f)
            return f

        return inner

    def run(self):
        scheduled = self.tasks.sort()
        completed = {}

        for task in scheduled:
            for node, values in self.tasks.graph.items():
                if task in values:
                    completed[task] = task(completed[node])
            if task not in completed:
                completed[task] = task()
        return completed


if __name__ == "__main__":
    # Illustration 1
    # --------------

    dag = DAG()
    dag.add(1)
    dag.add(1, 2)
    dag.add(1, 3)
    dag.add(1, 4)
    dag.add(3, 5)
    dag.add(2, 6)
    dag.add(4, 7)
    dag.add(5, 7)
    dag.add(6, 7)
    dag.in_degrees()
    dependencies = dag.sort()
    print(dependencies)

    # Illustration 2
    # --------------

    pipeline = Pipeline()


    @pipeline.task(depends_on=None)
    def first():
        return 20


    @pipeline.task(depends_on=first)
    def second(x):
        return x * 2


    @pipeline.task(depends_on=second)
    def third(x):
        return x // 3


    @pipeline.task(depends_on=second)
    def fourth(x):
        return x // 4


    graph = pipeline.tasks.graph
    print(graph)
    outputs = pipeline.run()
    print(outputs)
