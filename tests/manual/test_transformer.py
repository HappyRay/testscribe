from test_scribe.transformer import transform_value


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
