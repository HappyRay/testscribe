import test_scribe.model_type
import test_scribe.patcher
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.model import create_new_all_tests, get_exception_model, get_patch_models


def test_create_new_all_tests_update_test():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    new_test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    all_tests.tests = [m_test_model]
    all_tests.module = 'm'
    new_test.target_class_name = 'c'
    new_test.target_func_name = 'f'
    new_test.name = 't'
    result = create_new_all_tests(all_tests=all_tests, index_of_test_to_update=0, new_test=new_test)
    assert isinstance(result, test_scribe.model_type.AllTests)
    assert result.module == 'm'
    assert result.tests == [new_test]
    assert result.name_to_index == {'t': 0}
    all_tests.assert_not_called()
    new_test.assert_not_called()
    m_test_model.assert_not_called()


def test_create_new_all_tests_add_test():
    all_tests: test_scribe.model_type.AllTests = create_autospec(spec=test_scribe.model_type.AllTests)
    new_test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    all_tests.tests = []
    all_tests.module = 'm'
    new_test.name = 't'
    new_test.target_class_name = 'c'
    new_test.target_func_name = 'f'
    result = create_new_all_tests(all_tests=all_tests, index_of_test_to_update=-1, new_test=new_test)
    assert isinstance(result, test_scribe.model_type.AllTests)
    assert result.module == 'm'
    assert result.tests == [new_test]
    assert result.name_to_index == {'t': 0}
    all_tests.assert_not_called()
    new_test.assert_not_called()


def test_get_exception_model_no_exception():
    result = get_exception_model(exception=None)
    assert result is None


def test_get_exception_model_has_exception():
    result = get_exception_model(exception=TypeError("a"))
    assert isinstance(result, test_scribe.model_type.ExceptionModel)
    assert repr(result) == "ExceptionModel(type='TypeError', message='a')"


def test_get_patch_models():
    m_patcher: test_scribe.patcher.Patcher = create_autospec(spec=test_scribe.patcher.Patcher)
    m_patcher_1: test_scribe.patcher.Patcher = create_autospec(spec=test_scribe.patcher.Patcher)
    m_patcher.target = 't1'
    m_patcher.replacement_spec = 1
    m_patcher_1.target = 't2'
    m_patcher_1.replacement_spec = 2
    result = get_patch_models(patches=[m_patcher, m_patcher_1])
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.PatchModel)
    assert repr(result[0]) == "PatchModel(target='t1', replacement=1)"
    assert isinstance(result[1], test_scribe.model_type.PatchModel)
    assert repr(result[1]) == "PatchModel(target='t2', replacement=2)"
    m_patcher.assert_not_called()
    m_patcher_1.assert_not_called()
