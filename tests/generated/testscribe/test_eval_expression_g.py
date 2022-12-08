import test_data.simple
import testscribe.api.mock_api
import testscribe.error
import typing
from unittest.mock import patch
import pytest
from testscribe.eval_expression import contain_mock_proxy, eval_with_injected_names, expand_class_alias, expand_one_string_alias, expand_string_aliases, get_normalized_item_types, is_m_function_in_expression, process_mock_marker, process_mock_marker_dict, process_mock_marker_list, process_mock_marker_tuple, wrap_input_value


def test_contain_mock_proxy_false():
    result = contain_mock_proxy(value=[1, 2])
    assert result is False


def test_eval_with_injected_names():
    with patch('testscribe.eval_expression.global_var.g_name_mock_dict', {'a': 2}):
        result = eval_with_injected_names(expression='(a, m, test_data.simple.INT_VALUE)')
    assert result == (2, testscribe.api.mock_api.m, 1)


def test_expand_class_alias_class_without_c_alias():
    result = expand_class_alias(t=typing.Optional[test_data.simple.C], expression='None')
    assert result == 'None'


def test_expand_class_alias_class():
    result = expand_class_alias(t=typing.Optional[test_data.simple.C], expression='c(1)')
    assert result == 'test_data.simple.C(1)'


def test_expand_class_alias_not_a_class_type():
    result = expand_class_alias(t=str, expression='c1')
    assert result == 'c1'


def test_expand_one_string_alias_beginning_of_the_string():
    result = expand_one_string_alias(expression='A.foo', alias='A', full_str='abc')
    assert result == 'abc.foo'


def test_expand_one_string_alias_no_alias_in_input():
    result = expand_one_string_alias(expression='A.foo', alias='B', full_str='abc')
    assert result == 'A.foo'


def test_expand_one_string_alias_alias_not_by_itself():
    result = expand_one_string_alias(expression='Ab', alias='A', full_str='abc')
    assert result == 'Ab'


def test_expand_one_string_alias_alias_in_the_middle():
    result = expand_one_string_alias(expression='1 + A.foo()', alias='A', full_str='abc')
    assert result == '1 + abc.foo()'


def test_expand_one_string_alias_alias_at_the_end():
    result = expand_one_string_alias(expression='so.A', alias='A', full_str='abc')
    assert result == 'so.abc'


def test_expand_one_string_alias_full_test_is_a_number_string():
    result = expand_one_string_alias(expression='1 + A', alias='A', full_str='2')
    assert result == '1 + 2'


def test_expand_string_aliases():
    with patch('testscribe.eval_expression.g_aliases', {'a': 'hello', 'b': 'World'}):
        result = expand_string_aliases(expression='a-b')
    assert result == 'hello-World'


def test_get_normalized_item_types_tuple_with_ellipsis():
    result = get_normalized_item_types(t=typing.Tuple[int, ...], v=(1, 2))
    assert result == (int, int)


def test_is_m_function_in_expression_m_function():
    result = is_m_function_in_expression(expression='[ m (test_data.simple.C)]')
    assert result is True


def test_is_m_function_in_expression_no_m_function():
    result = is_m_function_in_expression(expression='("am", "m", bm())')
    assert result is False


def test_process_mock_marker_tuple_without_element_type():
    result = process_mock_marker(t=typing.Tuple, v=(1, 2))
    assert result == (1, 2)


def test_process_mock_marker_list_without_element_type():
    result = process_mock_marker(t=typing.List, v=[1])
    assert result == [1]


def test_process_mock_marker_no_mock_in_input():
    result = process_mock_marker(t=typing.Any, v=1)
    assert result == 1


def test_process_mock_marker_input_tuple_size_not_match_type():
    """
    Input expression doesn't match the type should throw an exception
    """
    with pytest.raises(testscribe.error.InputError) as exception_info:
        process_mock_marker(t=typing.Tuple[int, str], v=(1, 2, 3))
    assert str(exception_info.value) == "tuple value ((1, 2, 3)) size doesn't match the tuple type (typing.Tuple[int, str])."


def test_process_mock_marker_type_mismatch_throw_error():
    with pytest.raises(testscribe.error.InputError) as exception_info:
        process_mock_marker(t=typing.Tuple[int, int], v=(testscribe.api.mock_api.m, 1))
    assert str(exception_info.value) == "The type (<class 'int'>) can't be mocked."


def test_process_mock_marker_dict_not_dict_type():
    result = process_mock_marker_dict(t=typing.Any, v=1)
    assert result == 1


def test_process_mock_marker_list_not_list_type():
    result = process_mock_marker_list(t=typing.Any, v=1)
    assert result == 1


def test_process_mock_marker_tuple_not_tuple_type():
    result = process_mock_marker_tuple(t=typing.Any, v=1)
    assert result == 1


def test_wrap_input_value_simple():
    result = wrap_input_value(expression='a', v=1)
    assert result == 1
