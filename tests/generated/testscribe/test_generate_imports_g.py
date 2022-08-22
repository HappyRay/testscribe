import testscribe.model_type
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.generate_imports import gather_import_statement_for_exception_support, gather_import_statement_for_patch_support, gather_import_statements_for_mock_support, gather_import_statements_for_test_targets, generate_import_statement_str, get_target_for_a_test, need_exception_support, need_mock_support


def test_gather_import_statements_for_exception_support_has_exception():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_exception_model: testscribe.model_type.ExceptionModel = create_autospec(spec=testscribe.model_type.ExceptionModel)
    m_test_model.exception = m_exception_model
    result = gather_import_statement_for_exception_support(tests=[m_test_model, m_test_model_1])
    assert result == 'import pytest'
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
    m_exception_model.assert_not_called()


def test_gather_import_statements_for_exception_support_no_exception():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.exception = None
    result = gather_import_statement_for_exception_support(tests=[m_test_model])
    assert result == ''
    m_test_model.assert_not_called()


def test_gather_import_statement_for_patch_support_has_patch():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_test_model.patches = [m_patch_model]
    result = gather_import_statement_for_patch_support(tests=[m_test_model])
    assert result == 'from unittest.mock import patch'
    m_test_model.assert_not_called()
    m_patch_model.assert_not_called()


def test_gather_import_statement_for_patch_support_no_patch():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.patches = []
    result = gather_import_statement_for_patch_support(tests=[m_test_model])
    assert result == ''
    m_test_model.assert_not_called()


def test_gather_import_statements_for_mock_support_has_mock():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_test_model.mocks = [m_mock_model]
    result = gather_import_statements_for_mock_support(tests=[m_test_model])
    assert result == ['from testscribe.api.mock_api import get_normalized_mock_calls', 'from unittest.mock import ANY, call, create_autospec']
    m_test_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_gather_import_statements_for_mock_support_no_mock():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.mocks = []
    result = gather_import_statements_for_mock_support(tests=[m_test_model])
    assert result == []
    m_test_model.assert_not_called()


def test_gather_import_statements_for_test_targets():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    all_tests.module = 'm'
    m_test_model.target_class_name = 'b'
    m_test_model_1.target_class_name = ''
    m_test_model_1.target_func_name = 'a'
    result = gather_import_statements_for_test_targets(all_tests=all_tests)
    assert result == 'from m import a, b'
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_generate_import_statements():
    """
    Should combine statements and add a new line. Can also mock the calls if they were not used by the tool itself.
    """
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    all_tests.tests = [m_test_model]
    all_tests.module = 'a.target'
    m_test_model.mocks = [m_mock_model]
    m_test_model.exception = None
    m_test_model.result = 1
    m_test_model.init_parameters = None
    m_test_model.parameters = None
    m_test_model.patches = []
    m_test_model.target_class_name = ''
    m_test_model.target_func_name = 'func'
    m_mock_model.spec_str = 'a.b.m'
    m_mock_model.attributes = {}
    m_mock_model.calls = []
    result = generate_import_statement_str(all_tests=all_tests)
    assert result == """\
import a.b
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from a.target import func
"""
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_get_target_for_a_test_func():
    t: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    t.target_class_name = ''
    t.target_func_name = 'f'
    result = get_target_for_a_test(t=t)
    assert result == 'f'
    t.assert_not_called()


def test_get_target_for_a_test_class():
    t: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    t.target_class_name = 'B'
    result = get_target_for_a_test(t=t)
    assert result == 'B'
    t.assert_not_called()


def test_need_exception_support_has_exception():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_exception_model: testscribe.model_type.ExceptionModel = create_autospec(spec=testscribe.model_type.ExceptionModel)
    m_test_model.exception = None
    m_test_model_1.exception = m_exception_model
    result = need_exception_support(tests=[m_test_model, m_test_model_1])
    assert result is True
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
    m_exception_model.assert_not_called()


def test_need_exception_support_no_exception():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.exception = None
    m_test_model_1.exception = None
    result = need_exception_support(tests=[m_test_model, m_test_model_1])
    assert result is False
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_need_mock_support_has_mock():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_test_model.mocks = []
    m_test_model_1.mocks = [m_mock_model]
    result = need_mock_support(tests=[m_test_model, m_test_model_1])
    assert result is True
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
    m_mock_model.assert_not_called()


def test_need_mock_support_no_mock():
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model.mocks = []
    m_test_model_1.mocks = []
    result = need_mock_support(tests=[m_test_model, m_test_model_1])
    assert result is False
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
