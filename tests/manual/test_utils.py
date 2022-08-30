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
