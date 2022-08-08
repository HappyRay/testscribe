from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.util import consistent_hash_str, convert_camel_case_to_snake_case, flattern_list, generic_transform, remove_trailing_numbers


def test_consistent_hash_str():
    result = consistent_hash_str(s='a')
    assert result == 16955237001963240173058271559858726497


def test_convert_camel_case_to_snake_case():
    result = convert_camel_case_to_snake_case(s='FooBar')
    assert result == 'foo_bar'


def test_flattern_list():
    result = flattern_list(list_of_list=[['a'], ['b', 'c']])
    assert result == ['a', 'b', 'c']


def test_generic_transform_int():
    transform_func: callable = create_autospec(spec=callable)
    transform_func.return_value = 3
    result = generic_transform(v=1, transform_func=transform_func)
    assert result == 3
    transform_func_mock_calls = get_normalized_mock_calls(transform_func, callable)
    assert transform_func_mock_calls == [
        call(obj=1),
    ]


def test_generic_transform_dict():
    transform_func: callable = create_autospec(spec=callable)
    transform_func.side_effect = [1, 2, 3, 4, 5]
    result = generic_transform(v={'a': True, 'c': False}, transform_func=transform_func)
    assert result == 5
    transform_func_mock_calls = get_normalized_mock_calls(transform_func, callable)
    assert transform_func_mock_calls == [
        call(obj='a'),
        call(obj=True),
        call(obj='c'),
        call(obj=False),
        call(obj={1: 2, 3: 4}),
    ]


def test_generic_transform_set():
    transform_func: callable = create_autospec(spec=callable)
    transform_func.side_effect = [3, 4, 5]
    result = generic_transform(v=set([1, 2]), transform_func=transform_func)
    assert result == 5
    transform_func_mock_calls = get_normalized_mock_calls(transform_func, callable)
    assert transform_func_mock_calls == [
        call(obj=1),
        call(obj=2),
        call(obj=ANY),
    ]
    assert isinstance(transform_func_mock_calls[2].kwargs['obj'], set)
    assert sorted(list(transform_func_mock_calls[2].kwargs['obj'])) == [3, 4]


def test_generic_transform_tuple():
    transform_func: callable = create_autospec(spec=callable)
    transform_func.side_effect = [3, 4, 5]
    result = generic_transform(v=(1, 2), transform_func=transform_func)
    assert result == 5
    transform_func_mock_calls = get_normalized_mock_calls(transform_func, callable)
    assert transform_func_mock_calls == [
        call(obj=1),
        call(obj=2),
        call(obj=(3, 4)),
    ]


def test_generic_transform_list():
    transform_func: callable = create_autospec(spec=callable)
    transform_func.side_effect = [3, 4, 5]
    result = generic_transform(v=[1, 2], transform_func=transform_func)
    assert result == 5
    transform_func_mock_calls = get_normalized_mock_calls(transform_func, callable)
    assert transform_func_mock_calls == [
        call(obj=1),
        call(obj=2),
        call(obj=[3, 4]),
    ]


def test_remove_trailing_numbers_trailing_numbers():
    result = remove_trailing_numbers(s='a_12')
    assert result == 'a'


def test_remove_trailing_numbers_without_trailing_numbers():
    result = remove_trailing_numbers(s='a')
    assert result == 'a'


def test_remove_trailing_numbers_number_in_middle():
    result = remove_trailing_numbers(s='a1b')
    assert result == 'a1b'


def test_remove_trailing_numbers_trailing_number_without_underscore():
    result = remove_trailing_numbers(s='a1')
    assert result == 'a1'
