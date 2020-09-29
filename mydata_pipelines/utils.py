# Using a closure, recreate the partial() function:

# Example 1:


def add(a, b):
    return a + b


def c_partial(func, *args):
    # Enclosing Scope
    # Positional Arguments
    parent_args = args

    def inner(*inner_args):
        return func(*(parent_args + inner_args))

    return inner


add_two = c_partial(add, 2)
print(add_two(7))


# Example 2:
def catch_error(func):
    def inner(*args):
        try:
            return func(*args)
        except Exception as e:
            return e

    return inner


@catch_error
def throws_error():
    raise Exception("Throws Error")


print(throws_error())
