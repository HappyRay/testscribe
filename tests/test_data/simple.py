from dataclasses import dataclass
from types import ModuleType
from typing import Callable, Optional

INT_VALUE = 1


class Dummy:
    pass


@dataclass
class DataClassWithSimpleObject:
    d: Dummy


@dataclass
class SimpleDataClass:
    a: int
    s: str = None


@dataclass(frozen=True)
class ReadOnlyData:
    a: int


def foo(a: int) -> int:
    return a + 1


# Intentionally not making this class a dataclass
# to test the behavior of non dataclasses.
class C:
    a: int
    b: Optional[str] = None

    def __init__(self, a: int):
        self.a = a

    def bar(self, a: int) -> int:
        return self.a + a

    def __eq__(self, other):
        if not isinstance(other, C):
            return False
        elif self is other:
            return True
        else:
            return self.a == other.a


class D:
    def __init__(self, a):
        self.a = a


class WithClassMembers:
    def __init__(self, c: C):
        self.c = c


class FuncMember:
    def __init__(self, f: Callable):
        self.f = f


class ModuleMember:
    def __init__(self, m: ModuleType):
        self.m = m


class CallableClass:
    def __init__(self, i: int):
        self.i = i

    def __call__(self, *args, **kwargs):
        self.i += 1


class CustomReprStr:
    a: int

    def __init__(self, a: int):
        self.a = a

    def __repr__(self):
        return f"CustomReprStr({self.a})"

    def __str__(self):
        """
        Make it different from __repr__ for testing transform_class
        """
        return f"CustomReprStr instance member a: {self.a})"
