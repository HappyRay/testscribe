import inspect
import test_data.calculator
import test_data.class_method
import test_data.person
import test_data.service
import test_data.simple
import test_data.static_method
import test_data.with_future_annotation_import
import test_data.without_future_annotation_import
import test_scribe.error
import typing
import pytest
from test_scribe.reflection_util import get_bound_arguments, get_full_spec_name, get_method, get_method_signature_for_caller, get_module_and_symbol, get_module_str, get_module_str_from_object, get_param_list, get_return_type, get_symbol, get_type_name, get_typing_callable_return_type, has_param_names, is_instance_method, is_method, remove_brackets


def test_get_bound_arguments():
    result = get_bound_arguments(sig=inspect.signature(test_data.calculator.add), args=[1], kwargs={'b': 2})
    assert result == {'a': 1, 'b': 2}


def test_get_full_spec_name_function():
    result = get_full_spec_name(t=test_data.simple.foo)
    assert result == 'test_data.simple.foo'


def test_get_full_spec_name_callable():
    result = get_full_spec_name(t=typing.Callable)
    assert result == 'typing.Callable'


def test_get_full_spec_name_builtin_type():
    result = get_full_spec_name(t=Exception)
    assert result == 'Exception'


def test_get_full_spec_name_class():
    result = get_full_spec_name(t=test_data.person.Person)
    assert result == 'test_data.person.Person'


def test_get_method_non_method_member():
    result = get_method(clazz=test_data.simple.C, method_name='a')
    assert result is None


def test_get_method_invalid_method_name():
    result = get_method(clazz=test_data.simple.C, method_name='invalid')
    assert result is None


def test_get_method_valid_method():
    result = get_method(clazz=test_data.simple.C, method_name='bar')
    assert result == test_data.simple.C.bar


def test_get_method_signature_for_caller_invalid_method_name():
    with pytest.raises(test_scribe.error.Error) as exception_info:
        get_method_signature_for_caller(clazz=test_data.service.Service, name='invalid')
    assert "invalid is not a method of the class <class 'test_data.service.Service'>" == str(exception_info.value)


def test_get_method_signature_for_caller_static_method():
    result = get_method_signature_for_caller(clazz=test_data.static_method.StaticService, name='do')
    assert isinstance(result, inspect.Signature)
    assert repr(result) == '<Signature () -> int>'


def test_get_method_signature_for_caller_instance_method():
    result = get_method_signature_for_caller(clazz=test_data.service.Service, name='search_a_name')
    assert isinstance(result, inspect.Signature)
    assert repr(result) == '<Signature (keyword: str) -> str>'


def test_get_module_and_symbol_callable_with_component_types():
    result = get_module_and_symbol(full_name='typing.Callable[[typing.Any], bool]')
    assert result == ('typing', 'Callable')


def test_get_module_and_symbol_default_module():
    result = get_module_and_symbol(full_name='c')
    assert result == ('', 'c')


def test_get_module_and_symbol():
    result = get_module_and_symbol(full_name='a.b.c')
    assert result == ('a.b', 'c')


def test_get_module_str_empty_module_name():
    result = get_module_str(full_name='a')
    assert result == ''


def test_get_module_str():
    result = get_module_str(full_name='a.b.c')
    assert result == 'a.b'


def test_get_module_str_from_object_has_module():
    result = get_module_str_from_object(obj=test_data.simple.C)
    assert result == 'test_data.simple'


def test_get_module_str_from_object_no_module_attribute():
    result = get_module_str_from_object(obj=1)
    assert result == ''


def test_get_param_list_constructor_with_future_annotation_import():
    result = get_param_list(func=test_data.with_future_annotation_import.C2)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], inspect.Parameter)
    assert repr(result[0]) == '<Parameter "a: int">'


def test_get_param_list_constructor_without_future_annotation_import():
    result = get_param_list(func=test_data.without_future_annotation_import.C1)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], inspect.Parameter)
    assert repr(result[0]) == '<Parameter "a: int">'


def test_get_param_list_method_with_future_annotation_import():
    result = get_param_list(func=test_data.with_future_annotation_import.C2(1).m2)
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], inspect.Parameter)
    assert repr(result[0]) == '<Parameter "a: int">'
    assert isinstance(result[1], inspect.Parameter)
    assert repr(result[1]) == '<Parameter "b: str">'
    assert isinstance(result[2], inspect.Parameter)
    assert repr(result[2]) == '<Parameter "c: test_data.without_future_annotation_import.C0">'


def test_get_param_list_func_with_future_annotation_import():
    result = get_param_list(func=test_data.with_future_annotation_import.f2)
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], inspect.Parameter)
    assert repr(result[0]) == '<Parameter "a: int">'
    assert isinstance(result[1], inspect.Parameter)
    assert repr(result[1]) == '<Parameter "b: str">'
    assert isinstance(result[2], inspect.Parameter)
    assert repr(result[2]) == '<Parameter "c: test_data.without_future_annotation_import.C0">'


def test_get_param_list_method_without_future_annotation_import():
    result = get_param_list(func=test_data.without_future_annotation_import.C1(1).m1)
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], inspect.Parameter)
    assert repr(result[0]) == '<Parameter "a: int">'
    assert isinstance(result[1], inspect.Parameter)
    assert repr(result[1]) == '<Parameter "b: str">'
    assert isinstance(result[2], inspect.Parameter)
    assert repr(result[2]) == '<Parameter "c: test_data.without_future_annotation_import.C0">'


def test_get_param_list_func_without_future_annotation_import():
    result = get_param_list(func=test_data.without_future_annotation_import.f1)
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], inspect.Parameter)
    assert repr(result[0]) == '<Parameter "a: int">'
    assert isinstance(result[1], inspect.Parameter)
    assert repr(result[1]) == '<Parameter "b: str">'
    assert isinstance(result[2], inspect.Parameter)
    assert repr(result[2]) == '<Parameter "c: test_data.without_future_annotation_import.C0">'


def test_get_return_type_no_return_annotation():
    result = get_return_type(func=test_data.with_future_annotation_import.no_return_annotation_f)
    assert result == inspect._empty


def test_get_symbol_invalid():
    with pytest.raises(test_scribe.error.Error) as exception_info:
        get_symbol(full_name='test_data.simple.invalid')
    assert 'test_data.simple.invalid is not a valid identifier.' == str(exception_info.value)


def test_get_symbol_valid_symbol():
    result = get_symbol(full_name='test_data.simple.foo')
    assert result == test_data.simple.foo


def test_get_type_name_none_type():
    result = get_type_name(t=type(None))
    assert result == 'NoneType'


def test_get_type_name_dict():
    result = get_type_name(t=dict)
    assert result == 'dict'


def test_get_type_name_set():
    result = get_type_name(t=set)
    assert result == 'set'


def test_get_type_name_tuple():
    result = get_type_name(t=tuple)
    assert result == 'tuple'


def test_get_type_name_list():
    result = get_type_name(t=list)
    assert result == 'list'


def test_get_type_name_class():
    result = get_type_name(t=test_data.person.Person)
    assert result == 'test_data.person.Person'


def test_get_type_name_any():
    result = get_type_name(t=typing.Any)
    assert result == 'any'


def test_get_type_name_float():
    result = get_type_name(t=float)
    assert result == 'float'


def test_get_type_name_bool():
    result = get_type_name(t=bool)
    assert result == 'bool'


def test_get_type_name_int():
    result = get_type_name(t=int)
    assert result == 'int'


def test_get_type_name_str():
    result = get_type_name(t=str)
    assert result == 'str'


def test_get_typing_callable_return_type_no_return_type():
    result = get_typing_callable_return_type(t=typing.Callable)
    assert result == inspect._empty


def test_get_typing_callable_return_type_has_type_annotation():
    result = get_typing_callable_return_type(t=typing.Callable[[str] ,int])
    assert result == int


def test_has_param_names_negative_1():
    result = has_param_names(spec=typing.Callable[[int], int])
    assert result is False


def test_has_param_names_negative():
    result = has_param_names(spec=typing.Callable)
    assert result is False


def test_has_param_names_positive_func():
    result = has_param_names(spec=test_data.simple.foo)
    assert result is True


def test_has_param_names_positive():
    result = has_param_names(spec=test_data.simple.C)
    assert result is True


def test_is_instance_method_invalid_method_name():
    result = is_instance_method(clazz=test_data.simple.foo, method_name='')
    assert result is False


def test_is_instance_method_instance():
    result = is_instance_method(clazz=test_data.service.Service, method_name='search_a_name')
    assert result is True


def test_is_instance_method_static():
    result = is_instance_method(clazz=test_data.static_method.StaticService, method_name='do')
    assert result is False


def test_is_instance_method_class():
    result = is_instance_method(clazz=test_data.class_method.ClassService, method_name='do')
    assert result is False


def test_is_method_positive():
    result = is_method(clazz=test_data.simple.C, name='bar')
    assert result is True


def test_is_method_negative():
    result = is_method(clazz=test_data.simple.C, name='a')
    assert result is False


def test_remove_brackets_no_bracket():
    result = remove_brackets(full_name='str')
    assert result == 'str'


def test_remove_brackets_has_bracket():
    result = remove_brackets(full_name='typing.Callable[[typing.Any], bool]')
    assert result == 'typing.Callable'
