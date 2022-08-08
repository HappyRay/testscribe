from __future__ import annotations


class Resource:
    def __init__(self, name: str):
        self.name = name

    def do_somthing(self) -> None:
        print(f"Did something with {self.name}")


class Gate:
    def __init__(self, name: str):
        self.name = name
        self.resource = Resource(name)

    def __enter__(self) -> Resource:
        print(f"Enter {self.name}")
        return self.resource

    def __exit__(self, type, value, traceback) -> bool:
        print(f"Exit {self.name}")
        return True

# todo: create an example of how to handle a context manager implemented with
#  @contextmanager
#  https://book.pythontips.com/en/latest/context_managers.html


def use_resource(g: Gate):
    with g("a") as r:
        r.do_somthing()
