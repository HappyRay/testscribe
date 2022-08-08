from typing import (
    Any,
    List,
    Callable,
    Tuple,
    Dict,
    NamedTuple,
    TypedDict,
    FrozenSet,
    DefaultDict,
    OrderedDict,
    ChainMap,
    Counter,
    Deque,
)

from pytest import mark

from test_data.simple import foo
from test_scribe.type_util import is_class_type, is_container_type

"""
These tests can also be generated.
These manual tests are slightly more compact and relatively easy to write.
"""


class Foo:
    a = 1

    def m(self):
        pass


@mark.parametrize(
    "t",
    [
        bool,
        int,
        str,
        float,
        Any,
        type(foo),
        type(Foo.m),
        type(Foo().m),
    ],
)
def test_not_container_type(t: type):
    r = is_container_type(t)
    assert not r


@mark.parametrize(
    "t",
    [
        list,
        dict,
        tuple,
        set,
        List[int],
        Tuple[str, int],
        Dict[str, int],
        NamedTuple,
        TypedDict,
        FrozenSet,
        DefaultDict,
        OrderedDict,
        ChainMap,
        Counter,
        Deque,
    ],
)
def test_is_container_type(t: type):
    r = is_container_type(t)
    assert r


@mark.parametrize(
    "t",
    [
        bool,
        int,
        str,
        float,
        list,
        dict,
        tuple,
        set,
        Any,
        List[int],
        Tuple[str, int],
        Dict[str, int],
        type(foo),
        type(Foo.m),
        type(Foo().m),
    ],
)
def test_not_class_type(t: type):
    r = is_class_type(t)
    assert not r


@mark.parametrize("t", [Foo, Callable, Callable[[int], int]])
def test_class_type(t):
    r = is_class_type(Foo)
    assert r
