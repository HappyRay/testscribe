import click.termui
import pathlib
import test_data.simple
import testscribe.load_scribe_file
import testscribe.mocking_support
import testscribe.model_type
import testscribe.module
import testscribe.update_test_cmd
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from testscribe.update_test_cmd import create_patcher_from_model, create_patches_from_existing_test, get_expression_str, infer_output_root_dir_from_module, really_create_patcher_from_model, update_test_cmd


def test_create_patcher_from_model_skip():
    m_prompt: click.termui.prompt = create_autospec(spec=click.termui.prompt)
    patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_prompt.return_value = False
    patch_model.target = 'a.b'
    patch_model.replacement = 1
    with patch('testscribe.update_test_cmd.prompt', m_prompt):
        result = create_patcher_from_model(patch_model=patch_model, test=m_test_model)
    assert result is False
    m_prompt_mock_calls = get_normalized_mock_calls(m_prompt, click.termui.prompt)
    assert m_prompt_mock_calls == [
        call(text='Create patch with target ( a.b ) replacement ( 1 )?', default=True, type=bool),
    ]
    patch_model.assert_not_called()
    m_test_model.assert_not_called()


def test_create_patches_from_existing_test_recreate_all_patches():
    m_create_patcher_from_model: testscribe.update_test_cmd.create_patcher_from_model = create_autospec(spec=testscribe.update_test_cmd.create_patcher_from_model)
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_patch_model_1: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    test.patches = [m_patch_model, m_patch_model_1]
    with patch('testscribe.update_test_cmd.create_patcher_from_model', m_create_patcher_from_model):
        result = create_patches_from_existing_test(test=test)
    assert result is None
    m_create_patcher_from_model_mock_calls = get_normalized_mock_calls(m_create_patcher_from_model, testscribe.update_test_cmd.create_patcher_from_model)
    assert m_create_patcher_from_model_mock_calls == [
        call(patch_model=m_patch_model, test=test),
        call(patch_model=m_patch_model_1, test=test),
    ]
    test.assert_not_called()
    m_patch_model.assert_not_called()
    m_patch_model_1.assert_not_called()


def test_create_patches_from_existing_test_no_patch():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.patches = []
    result = create_patches_from_existing_test(test=test)
    assert result is None
    test.assert_not_called()


def test_get_expression_str_regular_value():
    result = get_expression_str(value=1)
    assert result == '1'


def test_get_expression_str_expression_model():
    result = get_expression_str(value=testscribe.model_type.ExpressionModel("a"))
    assert result == 'a'


def test_infer_output_root_dir_from_module():
    result = infer_output_root_dir_from_module(module=testscribe.module.Module(["a", "b", "m"]), scribe_file_path=pathlib.Path("root/a/b/m.tscribe"))
    assert isinstance(result, pathlib.PosixPath)
    assert repr(result) == "PosixPath('root')"


def test_really_create_patcher_from_model_mock():
    m_patch_with_mock_internal: testscribe.mocking_support.patch_with_mock_internal = create_autospec(spec=testscribe.mocking_support.patch_with_mock_internal)
    patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_patch_with_mock_internal.return_value = None
    patch_model.replacement = testscribe.model_type.MockNameModel("a_2")
    patch_model.target = 'a.b'
    m_test_model.mocks = [m_mock_model]
    m_mock_model.name = 'a_2'
    m_mock_model.spec_str = 'test_data.simple.C'
    with patch('testscribe.update_test_cmd.patch_with_mock_internal', m_patch_with_mock_internal):
        result = really_create_patcher_from_model(patch_model=patch_model, test=m_test_model)
    assert result is None
    m_patch_with_mock_internal_mock_calls = get_normalized_mock_calls(m_patch_with_mock_internal, testscribe.mocking_support.patch_with_mock_internal)
    assert m_patch_with_mock_internal_mock_calls == [
        call(target='a.b', mock_name='a', spec=test_data.simple.C),
    ]
    patch_model.assert_not_called()
    m_test_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_really_create_patcher_from_model_expression():
    m_patch_with_expression_internal: testscribe.mocking_support.patch_with_expression_internal = create_autospec(spec=testscribe.mocking_support.patch_with_expression_internal)
    patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_patch_with_expression_internal.return_value = None
    patch_model.replacement = 1
    patch_model.target = 'a.b'
    with patch('testscribe.update_test_cmd.patch_with_expression_internal', m_patch_with_expression_internal):
        result = really_create_patcher_from_model(patch_model=patch_model, test=m_test_model)
    assert result is None
    m_patch_with_expression_internal_mock_calls = get_normalized_mock_calls(m_patch_with_expression_internal, testscribe.mocking_support.patch_with_expression_internal)
    assert m_patch_with_expression_internal_mock_calls == [
        call(target_str='a.b', expression='1'),
    ]
    patch_model.assert_not_called()
    m_test_model.assert_not_called()


def test_update_test_cmd_no_such_test():
    m_load_scribe_file: testscribe.load_scribe_file.load_scribe_file = create_autospec(spec=testscribe.load_scribe_file.load_scribe_file)
    m_all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_load_scribe_file.return_value = m_all_tests
    m_all_tests.get_test_index_by_name.return_value = -1
    with patch('testscribe.update_test_cmd.load_scribe_file', m_load_scribe_file):
        result = update_test_cmd(scribe_file_path=pathlib.Path("a/b.tscribe"), test_name='t1')
    assert result == 1
    m_load_scribe_file_mock_calls = get_normalized_mock_calls(m_load_scribe_file, testscribe.load_scribe_file.load_scribe_file)
    assert m_load_scribe_file_mock_calls == [
        call(scribe_file=ANY),
    ]
    assert isinstance(m_load_scribe_file_mock_calls[0].kwargs['scribe_file'], pathlib.PosixPath)
    assert repr(m_load_scribe_file_mock_calls[0].kwargs['scribe_file']) == "PosixPath('a/b.tscribe')"
    m_all_tests_mock_calls = get_normalized_mock_calls(m_all_tests, testscribe.model_type.AllTests)
    assert m_all_tests_mock_calls == [
        call.get_test_index_by_name(test_name='t1'),
    ]
