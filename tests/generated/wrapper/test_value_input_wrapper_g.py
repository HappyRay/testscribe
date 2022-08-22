import testscribe.ignore
from wrapper.value_input_wrapper import post_process_raw_input_wrapper_special_value


def test_post_process_raw_input_wrapper_special_value():
    result = post_process_raw_input_wrapper_special_value()
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == 'ignore'
    assert isinstance(result[1], testscribe.ignore.IgnoreReturnValue)
    assert repr(result[1]) == "'Ignored'"
