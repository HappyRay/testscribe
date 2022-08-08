from test_data.set_handling import echo_set


def test_echo_set():
    result = echo_set(s=set([1, 2]))
    assert isinstance(result, set)
    assert sorted(list(result)) == [1, 2]
