from wrapper.repr_wrapper import obj_repr


def test_obj_repr_tuple():
    result = obj_repr(v=('a', 1))
    assert result == "('a', 1)"


def test_obj_repr_string():
    result = obj_repr(v='a')
    assert result == "'a'"
