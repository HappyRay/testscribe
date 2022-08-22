import testscribe.namedvalues
from testscribe.namedvalues import NamedValues, format_one_param


def test_as_arg_str():
    instance = NamedValues(name_value_list=[('', 1), ('b', 2)])
    result = instance.as_arg_str()
    assert result == '1, b=2'


def test_as_list():
    instance = NamedValues(name_value_list=testscribe.namedvalues.NamedValues([('a', 1)]))
    result = instance.as_list()
    assert result == [('a', 1)]


def test_get_size():
    instance = NamedValues(name_value_list=testscribe.namedvalues.NamedValues([('a', 1)]))
    result = instance.get_size()
    assert result == 1


def test_get_value_by_name_not_found():
    instance = NamedValues(name_value_list=testscribe.namedvalues.NamedValues([('a', 1)]))
    result = instance.get_value_by_name(name='b')
    assert result == testscribe.namedvalues.NameNotFound


def test_get_value_by_name_found():
    instance = NamedValues(name_value_list=testscribe.namedvalues.NamedValues([('a', 1)]))
    result = instance.get_value_by_name(name='a')
    assert result == 1


def test_format_one_param_no_name():
    result = format_one_param(name='', value=1)
    assert result == '1'


def test_format_one_param_has_name():
    result = format_one_param(name='a', value=1)
    assert result == 'a=1'
