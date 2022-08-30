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

from testscribe.transformer import transform_value


def test_trasform_value_makes_a_copy():
    """
    To test the transform_value function returns the transformed origial value.
    It's not affected by the changes made to the value.
    """
    v = [1]
    transformed = transform_value(v)
    # modify one of the values. This simulates the case when a parameter
    # is modified by the function being tested.
    v.append(2)
    assert v == [1, 2]
    assert transformed == [1]


def test_trasform_value_makes_a_deep_copy():
    """
    The generated test will compare values in this test.
    It's not suitable for comparing references.

    """
    list1 = [1]
    list2 = [list1, 2]
    r = transform_value(list2)
    assert r is not list2
    r[0] is not list1
