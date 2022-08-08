import test_data.simple
import test_scribe.ignore
import test_scribe.model_type
import test_scribe.user_triggered_exception
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.code_gen_util import add_indentation, add_indentation_to_str_list, collect_return_values, get_module_name, is_same_value, join_lines, pretty_format_repr_string, remove_empty, spec_contain_param_name_info, translate_special_mock_return_value


def test_add_indentation():
    result = add_indentation(s='ab\nc\nd', level=2)
    assert result == """\
        ab
        c
        d"""


def test_add_indentation_to_str_list_no_indent():
    result = add_indentation_to_str_list(lines=['a', 'bc'], level=0)
    assert result == ['a', 'bc']


def test_add_indentation_to_str_list_indent_2():
    result = add_indentation_to_str_list(lines=['a', 'bc'], level=2)
    assert result == ['        a', '        bc']


def test_collect_return_values():
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_mock_call_model_1: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_mock_call_model.return_value = 1
    m_mock_call_model_1.return_value = test_scribe.model_type.ExpressionModel("ignore")
    result = collect_return_values(mock_calls=[m_mock_call_model, m_mock_call_model_1])
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == 1
    assert isinstance(result[1], test_scribe.ignore.IgnoreReturnValue)
    assert repr(result[1]) == "'Ignored'"
    m_mock_call_model.assert_not_called()
    m_mock_call_model_1.assert_not_called()


def test_collect_return_values_none_is_preserved():
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_mock_call_model.return_value = None
    result = collect_return_values(mock_calls=[m_mock_call_model])
    assert result == [None]
    m_mock_call_model.assert_not_called()


def test_get_module_name_builtin_class():
    result = get_module_name(v=dict)
    assert result == ''


def test_get_module_name_class():
    result = get_module_name(v=test_data.simple.C(1))
    assert result == 'test_data.simple'


def test_get_module_name_4():
    result = get_module_name(v=1.1)
    assert result == ''


def test_get_module_name_3():
    result = get_module_name(v=None)
    assert result == ''


def test_get_module_name_2():
    result = get_module_name(v=True)
    assert result == ''


def test_get_module_name_1():
    result = get_module_name(v='s')
    assert result == ''


def test_get_module_name():
    result = get_module_name(v=1)
    assert result == ''


def test_is_same_value_not_same():
    result = is_same_value(values=[1, 2])
    assert result is False


def test_is_same_value_same():
    result = is_same_value(values=[1, 1, 1])
    assert result is True


def test_join_lines_indent():
    result = join_lines(lines=['a', 'bc'], prepend_new_line=False, indentation_level=1)
    assert result == """\
    a
    bc"""


def test_join_lines_empty_lines():
    result = join_lines(lines=['', ''], prepend_new_line=False, indentation_level=1)
    assert result == ''


def test_join_lines_filter_out_empty_strings():
    result = join_lines(lines=['', ''], prepend_new_line=True)
    assert result == ''


def test_join_lines_empty_with_prepend_new_line():
    result = join_lines(lines=[], prepend_new_line=True)
    assert result == ''


def test_join_lines_prepend_new_line():
    result = join_lines(lines=['a', 'bc'], prepend_new_line=True)
    assert result == """\

a
bc"""


def test_join_lines_no_prepend_new_line():
    result = join_lines(lines=['a', 'bc'], prepend_new_line=False)
    assert result == """\
a
bc"""


def test_pretty_format_repr_string_single_line():
    result = pretty_format_repr_string(s='a')
    assert result == "'a'"


def test_pretty_format_repr_string_multi_line():
    result = pretty_format_repr_string(s='a\nb')
    assert result == '"""\\\na\nb"""'


def test_pretty_format_repr_string_one_line_plus_one_empty_line():
    result = pretty_format_repr_string(s='ab\n')
    assert result == "'ab\\n'"


def test_pretty_format_repr_string_with_trailing_double_quote():
    """
    The trailing double quote should be escaped.
    """
    result = pretty_format_repr_string(s='a\nb"')
    assert result == '"""\\\na\nb\\""""'


def test_pretty_format_repr_string_multi_line_with_triple_double_quotes():
    """
    Don't use triple quotes format when the input contains triple double quotes itself.
    """
    result = pretty_format_repr_string(s='a\n"""')
    assert result == '\'a\\n"""\''


def test_remove_empty():
    result = remove_empty(a_list=['a', '', 'b', ''])
    assert result == ['a', 'b']


def test_spec_contain_param_name_info_collections_callable():
    result = spec_contain_param_name_info(spec_str='collections.Callable')
    assert result is False


def test_spec_contain_param_name_info_collections_abc_callable():
    result = spec_contain_param_name_info(spec_str='collections.abc.Callable')
    assert result is False


def test_spec_contain_param_name_info_callable():
    result = spec_contain_param_name_info(spec_str='typing.Callable')
    assert result is False


def test_spec_contain_param_name_info_positive():
    result = spec_contain_param_name_info(spec_str='test_data.simple.C')
    assert result is True


def test_translate_special_mock_return_value_ignore():
    result = translate_special_mock_return_value(value=test_scribe.model_type.ExpressionModel("ignore"))
    assert isinstance(result, test_scribe.ignore.IgnoreReturnValue)
    assert repr(result) == "'Ignored'"


def test_translate_special_mock_return_value_user_triggered_exception():
    result = translate_special_mock_return_value(value=test_scribe.model_type.ExpressionModel("throw(Exception())"))
    assert isinstance(result, test_scribe.user_triggered_exception.UserTriggeredException)
    assert repr(result) == 'Exception()'


def test_translate_special_mock_return_value_expression():
    result = translate_special_mock_return_value(value=test_scribe.model_type.ExpressionModel("1 + 2"))
    assert isinstance(result, test_scribe.model_type.ExpressionModel)
    assert repr(result) == '1 + 2'


def test_translate_special_mock_return_value_none():
    result = translate_special_mock_return_value(value=None)
    assert result is None


def test_translate_special_mock_return_value_regular():
    result = translate_special_mock_return_value(value=1)
    assert result == 1
