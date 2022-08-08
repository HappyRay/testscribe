import typing
import pytest
from test_scribe.value_input_cli import convert_str_to_bool, post_process_raw_input, transform_default_value_cli


def test_convert_str_to_bool_true_5():
    result = convert_str_to_bool(s='y')
    assert result is True


def test_convert_str_to_bool_true_4():
    result = convert_str_to_bool(s='yes')
    assert result is True


def test_convert_str_to_bool_true_3():
    result = convert_str_to_bool(s='t')
    assert result is True


def test_convert_str_to_bool_true_2():
    result = convert_str_to_bool(s='true')
    assert result is True


def test_convert_str_to_bool_true_1():
    result = convert_str_to_bool(s='on')
    assert result is True


def test_convert_str_to_bool_true():
    result = convert_str_to_bool(s='1')
    assert result is True


def test_convert_str_to_bool_false_5():
    result = convert_str_to_bool(s='n')
    assert result is False


def test_convert_str_to_bool_false_4():
    result = convert_str_to_bool(s='no')
    assert result is False


def test_convert_str_to_bool_false_3():
    result = convert_str_to_bool(s='f')
    assert result is False


def test_convert_str_to_bool_false_2():
    result = convert_str_to_bool(s='false')
    assert result is False


def test_convert_str_to_bool_false_1():
    result = convert_str_to_bool(s='off')
    assert result is False


def test_convert_str_to_bool_false():
    result = convert_str_to_bool(s='0')
    assert result is False


def test_convert_str_to_bool_invalid_input_raise_exception():
    with pytest.raises(ValueError) as exception_info:
        convert_str_to_bool(s='a')
    assert "invalid truth value 'a'" == str(exception_info.value)


def test_post_process_raw_input_int():
    result = post_process_raw_input(raw_input_str='1', t=int)
    assert result == 1


def test_post_process_raw_input_float():
    result = post_process_raw_input(raw_input_str='2.1', t=float)
    assert result == 2.1


def test_post_process_raw_input_bool():
    result = post_process_raw_input(raw_input_str='f', t=bool)
    assert result is False


def test_post_process_raw_input_str():
    result = post_process_raw_input(raw_input_str='f', t=str)
    assert result == 'f'


def test_post_process_raw_input_expression():
    result = post_process_raw_input(raw_input_str='[1 , 1+2]', t=list)
    assert result == [1, 3]


def test_transform_default_value_cli_str_not_str_type():
    result = transform_default_value_cli(default='a', t=typing.Any)
    assert result == "'a'"


def test_transform_default_value_cli_str_and_str_type():
    result = transform_default_value_cli(default='a', t=str)
    assert result == 'a'


def test_transform_default_value_cli_non_str():
    result = transform_default_value_cli(default=1, t=int)
    assert result == '1'
