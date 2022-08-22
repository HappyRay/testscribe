from typing import Tuple

from pytest import mark

from test_data.with_future_annotation_import import f2, C2
from test_data.without_future_annotation_import import f1, C1
from testscribe.reflection_util import (
    get_return_type,
)
from testscribe.type_util import get_type_args


def test_get_type_args_tuple_with_ellipsis():
    # Pyyaml has trouble saving the value Ellipsis
    # Thus this test has to be written manually.
    result = get_type_args(t=Tuple[int, ...])
    assert result == (int, Ellipsis)


@mark.parametrize(
    "func",
    [
        f1,
        f2,
        C1.m1,
        C2.m2,
    ],
)
def test_get_return_type(func):
    r = get_return_type(func=func)
    assert r == int
