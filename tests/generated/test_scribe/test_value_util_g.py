import test_scribe.value_util
from test_scribe.value_util import get_value, get_value_repr


def test_get_value_int():
    result = get_value(v=1)
    assert result == 1


def test_get_value_input_value():
    result = get_value(v=test_scribe.value_util.InputValue("a + 1", 2))
    assert result == 2


def test_get_value_repr_input_value():
    result = get_value_repr(v=test_scribe.value_util.InputValue("1+1", 2))
    assert result == '1+1'


def test_get_value_repr_str():
    result = get_value_repr(v='a')
    assert result == "'a'"


def test_get_value_repr_int():
    result = get_value_repr(v=1)
    assert result == '1'
