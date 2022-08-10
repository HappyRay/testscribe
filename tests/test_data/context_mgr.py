class Gate:

    def __enter__(self) -> int:
        print("Entering the context")
        return 1

    def __exit__(self, a_type, value, traceback) -> bool:
        print("Leaving the context")
        return True


# todo: create an example of how to handle a context manager implemented with
#  @contextmanager
#  https://book.pythontips.com/en/latest/context_managers.html


def use_resource(g: Gate):
    with g as r:
        return r
