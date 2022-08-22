import testscribe.module
from testscribe.module import Module, get_module_from_str


def test_get_module_name_only():
    instance = Module(module_names=['a', 'b'])
    result = instance.get_module_name_only()
    assert result == 'b'


def test_get_module_str():
    instance = Module(module_names=['a', 'b'])
    result = instance.get_module_str()
    assert result == 'a.b'


def test_get_package_name_list_builtin_name():
    instance = Module(module_names=['int'])
    result = instance.get_package_name_list()
    assert result == []


def test_get_package_name_list():
    instance = Module(module_names=['a', 'b', 'c'])
    result = instance.get_package_name_list()
    assert result == ['a', 'b']


def test_get_module_from_str():
    result = get_module_from_str(name='a.b.c')
    assert isinstance(result, testscribe.module.Module)
    assert result.names == ('a', 'b', 'c')
