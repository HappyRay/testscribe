def foo():
    pass


def return_fixed_func():
    return foo


def echo_func(f: callable):
    return f
