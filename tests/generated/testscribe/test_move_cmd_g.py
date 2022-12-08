import fixture.helper
import pathlib
import testscribe.config
import testscribe.error
import testscribe.model_type
import testscribe.module
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
import pytest
from testscribe.move_cmd import add_one_test, do_move, does_test_match_target_name, get_name_to_compare_with, get_output_root_path, get_tests_to_move_from_one_file, is_class_name, module_contain_same_symbol, search_tests_to_remove, should_skip_module


def test_add_one_test():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model]
    all_tests.module = 'a.b'
    test.name = 'test_f'
    test.short_name = '_'
    test.target_func_name = 'f'
    test.target_class_name = ''
    m_test_model.name = 'test_f'
    m_test_model.target_class_name = ''
    m_test_model.target_func_name = 'f'
    result = add_one_test(all_tests=all_tests, test=test)
    assert isinstance(result, testscribe.model_type.AllTests)
    assert result.module == 'a.b'
    assert result.tests == [test, m_test_model]
    assert result.name_to_index == {'test_f_1': 0, 'test_f': 1}
    all_tests.assert_not_called()
    test.assert_not_called()
    m_test_model.assert_not_called()


def test_do_move_no_test_to_move():
    result = do_move(module=testscribe.module.Module(["foo", "bar", "m"]), output_root_path=pathlib.Path("a/b"), tests_to_move=[])
    assert result is False


def test_does_test_match_target_name_negative():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.target_class_name = 'D'
    result = does_test_match_target_name(test=test, class_or_function_name='c', target_is_class=True)
    assert result is False
    test.assert_not_called()


def test_does_test_match_target_name_positive():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.target_func_name = 'f'
    result = does_test_match_target_name(test=test, class_or_function_name='f', target_is_class=False)
    assert result is True
    test.assert_not_called()


def test_get_name_to_compare_with_class():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.target_class_name = 'C'
    result = get_name_to_compare_with(target_is_class=True, test=test)
    assert result == 'C'
    test.assert_not_called()


def test_get_name_to_compare_with_func():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.target_func_name = 'f'
    result = get_name_to_compare_with(target_is_class=False, test=test)
    assert result == 'f'
    test.assert_not_called()


def test_get_output_root_path_via_config():
    m_config: testscribe.config.Config = create_autospec(spec=testscribe.config.Config)
    m_config.output_root_path = pathlib.Path("a/b")
    result = get_output_root_path(config=m_config, cmd_line_root_path=None)
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('a/b')"
    m_config.assert_not_called()


def test_get_output_root_path_via_cmd_line():
    m_config: testscribe.config.Config = create_autospec(spec=testscribe.config.Config)
    result = get_output_root_path(config=m_config, cmd_line_root_path=pathlib.Path("a/b"))
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('a/b')"
    m_config.assert_not_called()


def test_get_tests_to_move_from_one_file_no_matching_test():
    result = get_tests_to_move_from_one_file(class_or_function_name='f', target_is_class=False, scribe_file=fixture.helper.get_test_result_path()/"service.tscribe", target_module_str='a')
    assert result == []


def test_get_tests_to_move_from_one_file_skip():
    result = get_tests_to_move_from_one_file(class_or_function_name='f', target_is_class=False, scribe_file=fixture.helper.get_test_result_path()/"service.tscribe", target_module_str='test_data.service')
    assert result == []


def test_is_class_name_function():
    result = is_class_name(module_str='test_data.product', class_or_function_name='get_a_product_total')
    assert result is False


def test_is_class_name_method():
    with pytest.raises(testscribe.error.Error) as exception_info:
        is_class_name(module_str='test_data.product', class_or_function_name='create_sample_products')
    assert str(exception_info.value) == 'create_sample_products is not a valid function or class in the module test_data.product'


def test_is_class_name_class():
    result = is_class_name(module_str='test_data.product', class_or_function_name='Product')
    assert result is True


def test_is_class_name_non_exist_symbol():
    with pytest.raises(testscribe.error.Error) as exception_info:
        is_class_name(module_str='test_data.product', class_or_function_name='foo')
    assert str(exception_info.value) == 'foo is not a valid function or class in the module test_data.product'


def test_module_contain_same_symbol_method_should_not_match():
    result = module_contain_same_symbol(module_str='test_data.service', name='search_a_name', is_class=False, target_module_str='foo')
    assert result is False


def test_module_contain_same_symbol_not_exist_function():
    result = module_contain_same_symbol(module_str='test_data.calculator', name='f', is_class=False, target_module_str='foo')
    assert result is False


def test_module_contain_same_symbol_exist_function():
    result = module_contain_same_symbol(module_str='test_data.calculator', name='add', is_class=False, target_module_str='foo')
    assert result is True


def test_module_contain_same_symbol_not_exist_class():
    result = module_contain_same_symbol(module_str='test_data.service', name='C', is_class=True, target_module_str='foo')
    assert result is False


def test_module_contain_same_symbol_exist_class():
    result = module_contain_same_symbol(module_str='test_data.service', name='Service', is_class=True, target_module_str='foo')
    assert result is True


def test_module_contain_same_symbol_symbol_not_exist():
    result = module_contain_same_symbol(module_str='testscribe.value_input', name='foo', is_class=False, target_module_str='testscribe.util')
    assert result is False


def test_module_contain_same_symbol_import_same_symbol():
    """
    The same symbol is imported
    """
    result = module_contain_same_symbol(module_str='testscribe.value_input', name='remove_trailing_numbers', is_class=False, target_module_str='testscribe.util')
    assert result is False


def test_search_tests_to_remove():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_2: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_3: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.target_func_name = 'a'
    m_test_model_1.target_func_name = 'b'
    m_test_model_2.target_func_name = 'f'
    m_test_model_3.target_func_name = 'f'
    result = search_tests_to_remove(class_or_function_name='f', target_is_class=False, tests=[m_test_model, m_test_model_1, m_test_model_2, m_test_model_3])
    assert result == ([m_test_model, m_test_model_1], [m_test_model_2, m_test_model_3])
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
    m_test_model_2.assert_not_called()
    m_test_model_3.assert_not_called()


def test_should_skip_module_no_match():
    result = should_skip_module(module_str='test_data.service', class_or_function_name='foo', scribe_file=pathlib.Path(), target_is_class=False, target_module_str='a')
    assert result is False


def test_should_skip_module_same_symbol():
    result = should_skip_module(module_str='test_data.service', class_or_function_name='Service', scribe_file=pathlib.Path(), target_is_class=True, target_module_str='a')
    assert result is True


def test_should_skip_module_same_module():
    result = should_skip_module(module_str='a', class_or_function_name='f', scribe_file=pathlib.Path(), target_is_class=False, target_module_str='a')
    assert result is True
