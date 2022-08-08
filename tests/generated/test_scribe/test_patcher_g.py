import collections
from test_scribe.patcher import decrement_counter, remove_mock


def test_decrement_counter_only_one():
    result = decrement_counter(name_counter=collections.Counter({"a": 1}), nomalized_name='a')
    assert result == {}


def test_decrement_counter_more_than_1():
    result = decrement_counter(name_counter=collections.Counter({"a": 2}), nomalized_name='a')
    assert result == {'a': 1}


def test_remove_mock_not_a_mock():
    result = remove_mock(replacement_spec=1)
    assert result is None
