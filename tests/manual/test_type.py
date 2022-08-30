#  Copyright 2022 Ruiguo (Ray) Yang
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

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
from testscribe.type_util import is_class_type, is_container_type

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
