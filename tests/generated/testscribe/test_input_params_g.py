import pathlib
import test_data.greet
import test_data.simple
import testscribe.input_params
import testscribe.module
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from testscribe.input_params import create_input_params, create_output_dir_for_module, get_scribe_file_path, get_target_class_name, get_target_function_name


def test_create_input_params():
    result = create_input_params(module=testscribe.module.Module(["test_data", "greet"]), function_name='greet', output_root_dir=pathlib.Path("out/root"), ask_for_test_name=False, ask_for_description=True)
    assert isinstance(result, testscribe.input_params.InputParams)
    assert result.func == test_data.greet.Greeter.greet
    assert isinstance(result.output_root_dir, pathlib.PosixPath)
    assert repr(result.output_root_dir) == "PosixPath('out/root')"
    assert isinstance(result.module, testscribe.module.Module)
    assert result.module.names == ('test_data', 'greet')
    assert result.clazz == test_data.greet.Greeter
    assert result.ask_for_test_name is False
    assert result.ask_for_description is True


def test_create_output_dir_for_module():
    output_root_dir: pathlib.Path = create_autospec(spec=pathlib.Path)
    m_path: pathlib.Path = create_autospec(spec=pathlib.Path)
    output_root_dir.joinpath.return_value = m_path
    result = create_output_dir_for_module(output_root_dir=output_root_dir, module=testscribe.module.Module(["foo", "bar", "m"]))
    assert result is m_path
    output_root_dir_mock_calls = get_normalized_mock_calls(output_root_dir, pathlib.Path)
    assert output_root_dir_mock_calls == [
        call.joinpath(args=('foo', 'bar')),
    ]
    m_path_mock_calls = get_normalized_mock_calls(m_path, pathlib.Path)
    assert m_path_mock_calls == [
        call.mkdir(parents=True, exist_ok=True),
    ]


def test_get_scribe_file_path():
    m_create_output_dir_for_module: testscribe.input_params.create_output_dir_for_module = create_autospec(spec=testscribe.input_params.create_output_dir_for_module)
    m_create_output_dir_for_module.return_value = pathlib.Path("test_root/a")
    with patch('testscribe.input_params.create_output_dir_for_module', m_create_output_dir_for_module):
        result = get_scribe_file_path(output_root_dir=pathlib.Path("test_root"), module=testscribe.module.Module(["a", "b"]))
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('test_root/a/b.tscribe')"
    m_create_output_dir_for_module_mock_calls = get_normalized_mock_calls(m_create_output_dir_for_module, testscribe.input_params.create_output_dir_for_module)
    assert m_create_output_dir_for_module_mock_calls == [
        call(output_root_dir=ANY, module=ANY),
    ]
    assert isinstance(m_create_output_dir_for_module_mock_calls[0][2]['output_root_dir'], pathlib.PosixPath)
    assert repr(m_create_output_dir_for_module_mock_calls[0][2]['output_root_dir']) == "PosixPath('test_root')"
    assert isinstance(m_create_output_dir_for_module_mock_calls[0][2]['module'], testscribe.module.Module)
    assert m_create_output_dir_for_module_mock_calls[0][2]['module'].names == ('a', 'b')


def test_get_target_class_name_no_class():
    input_params: testscribe.input_params.InputParams = create_autospec(spec=testscribe.input_params.InputParams)
    input_params.clazz = None
    result = get_target_class_name(input_params=input_params)
    assert result == ''
    input_params.assert_not_called()


def test_get_target_class_name_has_class():
    input_params: testscribe.input_params.InputParams = create_autospec(spec=testscribe.input_params.InputParams)
    input_params.clazz = test_data.simple.C
    result = get_target_class_name(input_params=input_params)
    assert result == 'C'
    input_params.assert_not_called()


def test_get_target_function_name():
    input_params: testscribe.input_params.InputParams = create_autospec(spec=testscribe.input_params.InputParams)
    input_params.func = test_data.simple.foo
    result = get_target_function_name(input_params=input_params)
    assert result == 'foo'
    input_params.assert_not_called()
