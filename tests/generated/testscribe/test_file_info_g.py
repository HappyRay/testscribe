import fixture.helper
import test_data.calculator
import test_data.greet
import testscribe.error
import testscribe.module
import pytest
from testscribe.file_info import get_function, get_module


def test_get_function_method():
    result = get_function(module_name='test_data.greet', func_name='greet')
    assert result == (test_data.greet.Greeter.greet, test_data.greet.Greeter)


def test_get_function_valid_function():
    result = get_function(module_name='test_data.calculator', func_name='add')
    assert result == (test_data.calculator.add, None)


def test_get_function_throws_exception_non_existing_function():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_function(module_name='test_data.calculator', func_name='foo')
    assert "Can't find the function or method with the name foo in module test_data.calculator." == str(exception_info.value)


def test_get_function_throws_exception_non_function():
    with pytest.raises(testscribe.error.Error) as exception_info:
        get_function(module_name='test_data.calculator', func_name='dummy')
    assert "Can't find the function or method with the name dummy in module test_data.calculator." == str(exception_info.value)


def test_get_module():
    result = get_module(target_file=fixture.helper.get_absolute_path("test_data/calculator.py"))
    assert isinstance(result, testscribe.module.Module)
    assert result.names == ('test_data', 'calculator')
