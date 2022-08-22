import collections.abc
import test_data.simple
import typing
from testscribe.type_util import get_class_type, get_type_args, get_type_origin, is_a_class_instance, is_class_type, is_function_instance, is_function_type, is_primitive_container_type, is_primitive_type, is_spec_value, is_typing_callable_type, is_union_type


def test_get_class_type_union_with_multiple_classes():
    result = get_class_type(t=typing.Union[test_data.simple.Dummy, test_data.simple.C])
    assert result == test_data.simple.Dummy


def test_get_class_type_union_with_class():
    result = get_class_type(t=typing.Union[int, test_data.simple.C])
    assert result == test_data.simple.C


def test_optional_non_class():
    result = get_class_type(t=typing.Optional[int])
    assert result is None


def test_get_class_type_optional_class():
    result = get_class_type(t=typing.Optional[test_data.simple.C])
    assert result == test_data.simple.C


def test_get_class_type_class():
    result = get_class_type(t=test_data.simple.C)
    assert result == test_data.simple.C


def test_get_type_args_list_without_element_type():
    result = get_type_args(t=typing.List)
    assert result == ()


def test_get_type_args_list_of_string():
    result = get_type_args(t=typing.List[str])
    assert result == (str,)


def test_get_type_args():
    result = get_type_args(t=typing.Callable[[str] ,int])
    assert result == ([str], int)


def test_get_type_origin_1():
    result = get_type_origin(t=typing.List[str])
    assert result == list


def test_get_type_origin():
    result = get_type_origin(t=typing.List)
    assert result == list


def test_get_type_origin_list_has_no_origin():
    result = get_type_origin(t=list)
    assert result is None


def test_is_a_class_instance_false():
    result = is_a_class_instance(v=1)
    assert result is False


def test_is_a_class_instance_true():
    result = is_a_class_instance(v=test_data.simple.C(1))
    assert result is True


def test_is_class_type_union():
    result = is_class_type(t=typing.Union[int, str])
    assert result is False


def test_is_function_instance_int():
    result = is_function_instance(v=1)
    assert result is False


def test_is_function_instance_builtin_method_instance():
    result = is_function_instance(v=[].append)
    assert result is True


def test_is_function_instance_method_instance():
    result = is_function_instance(v=test_data.simple.C(1).bar)
    assert result is True


def test_is_function_instance_builtin_func():
    result = is_function_instance(v=len)
    assert result is True


def test_is_function_instance_func():
    result = is_function_instance(v=test_data.simple.foo)
    assert result is True


def test_is_function_type_callable_type():
    result = is_function_type(t=typing.Callable)
    assert result is False


def test_is_primitive_container_type_int():
    result = is_primitive_container_type(t=int)
    assert result is False


def test_is_primitive_container_type_set():
    result = is_primitive_container_type(t=set)
    assert result is True


def test_is_primitive_container_type_tuple():
    result = is_primitive_container_type(t=tuple)
    assert result is True


def test_is_primitive_container_type_dict():
    result = is_primitive_container_type(t=dict)
    assert result is True


def test_is_primitive_container_type_list():
    result = is_primitive_container_type(t=list)
    assert result is True


def test_is_primitive_type_func_type():
    result = is_primitive_type(t=type(test_data.simple.foo))
    assert result is True


def test_is_primitive_type_func():
    result = is_primitive_type(t=test_data.simple.foo)
    assert result is False


def test_is_primitive_type_float():
    result = is_primitive_type(t=float)
    assert result is True


def test_is_primitive_type_str():
    result = is_primitive_type(t=str)
    assert result is True


def test_is_primitive_type_bool():
    result = is_primitive_type(t=bool)
    assert result is True


def test_is_primitive_type_int():
    result = is_primitive_type(t=int)
    assert result is True


def test_is_spec_value_class_is_spec():
    result = is_spec_value(value=test_data.simple.C)
    assert result is True


def test_is_spec_value_func_is_spec():
    result = is_spec_value(value=test_data.simple.foo)
    assert result is True


def test_is_spec_value_int_not_spec():
    result = is_spec_value(value=1)
    assert result is False


def test_is_typing_callable_type_3():
    result = is_typing_callable_type(t=test_data.simple.C)
    assert result is False


def test_is_typing_callable_type_2():
    result = is_typing_callable_type(t=typing.Callable[[int], int])
    assert result is True


def test_is_typing_callable_type_1():
    result = is_typing_callable_type(t=typing.Callable)
    assert result is True


def test_is_typing_callable_type():
    result = is_typing_callable_type(t=collections.abc.Callable)
    assert result is True


def test_is_union_type_optional():
    result = is_union_type(t=typing.Optional[int])
    assert result is True


def test_is_union_type_true():
    result = is_union_type(t=typing.Union[int, str])
    assert result is True


def test_is_union_type_false():
    result = is_union_type(t=int)
    assert result is False
