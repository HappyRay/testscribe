from __future__ import annotations

from test_data.without_future_annotation_import import C0


class C2:
    def __init__(self, a: int):
        pass

    def m2(self, a: int, b: str, c: C0) -> int:
        pass


def f2(a: int, b: str, c: C0) -> int:
    pass


def no_return_annotation_f():
    pass
