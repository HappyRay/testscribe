import pathlib
import testscribe.execution_util
import testscribe.model
import testscribe.model_type
import testscribe.namedvalues
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from testscribe.generate_tests import gen_create_invocation_str, gen_invocation_str_with_exception, gen_invocation_str_with_patch, generate_create_instance_statement, generate_docstring, generate_invocation_statement, generate_mocks_str, generate_one_test_function, generate_result_assertion_str, generate_result_assignment_str, generate_target_instance_str, generate_tests_output_string, generate_unit_test_file, get_invocation_indent_level, wrap_exception_assertion


def test_gen_create_invocation_str():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.target_class_name = 'C'
    test.init_parameters = testscribe.namedvalues.NamedValues()
    test.parameters = testscribe.namedvalues.NamedValues()
    test.exception = None
    test.target_func_name = 'f'
    result = gen_create_invocation_str(test=test)
    assert result == """\
instance = C()
result = instance.f()"""
    test.assert_not_called()


def test_gen_invocation_str_with_exception():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.target_class_name = ''
    test.init_parameters = testscribe.namedvalues.NamedValues()
    test.parameters = testscribe.namedvalues.NamedValues()
    test.exception = testscribe.model_type.ExceptionModel("a.b.C", "msg")
    test.target_func_name = 'f'
    result = gen_invocation_str_with_exception(test=test)
    assert result == """\
with pytest.raises(a.b.C) as exception_info:
    f()
assert str(exception_info.value) == 'msg'"""
    test.assert_not_called()


def test_gen_invocation_str_with_patch():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    test.patches = [m_patch_model]
    test.target_class_name = 'C'
    test.init_parameters = testscribe.namedvalues.NamedValues()
    test.parameters = testscribe.namedvalues.NamedValues()
    test.exception = testscribe.model_type.ExceptionModel("a.b.C", "msg")
    test.target_func_name = 'f'
    m_patch_model.target = 't'
    m_patch_model.replacement = 1
    result = gen_invocation_str_with_patch(test=test)
    assert result == """\

    with patch('t', 1):
        with pytest.raises(a.b.C) as exception_info:
            instance = C()
            instance.f()
        assert str(exception_info.value) == 'msg'"""
    test.assert_not_called()
    m_patch_model.assert_not_called()


def test_generate_create_instance_statement_no_class():
    result = generate_create_instance_statement(target_class_name='', init_parameters=testscribe.namedvalues.NamedValues())
    assert result == ''


def test_generate_create_instance_statement():
    result = generate_create_instance_statement(target_class_name='Foo', init_parameters=testscribe.namedvalues.NamedValues([("a", 1), ("b", 2)]))
    assert result == 'instance = Foo(a=1, b=2)\n'


def test_generate_docstring_has_doc():
    result = generate_docstring(description='a b')
    assert result == '\n    """\n    a b\n    """'


def test_generate_docstring_no_doc():
    result = generate_docstring(description='')
    assert result == ''


def test_generate_invocation_statement_exception_in_constructor():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.parameters = None
    result = generate_invocation_statement(test=test)
    assert result == ''
    test.assert_not_called()


def test_generate_invocation_statement_method():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.parameters = testscribe.namedvalues.NamedValues([("a", 1)])
    test.target_class_name = 'C'
    test.exception = None
    test.target_func_name = 'f'
    result = generate_invocation_statement(test=test)
    assert result == 'result = instance.f(a=1)'
    test.assert_not_called()


def test_generate_mocks_single_mock_without_attributes_and_calls():
    input_mock: testscribe.model.MockModel = create_autospec(spec=testscribe.model.MockModel)
    input_mock.spec_str = 'spec'
    input_mock.name = 'm'
    input_mock.attributes = {}
    input_mock.calls = []
    result = generate_mocks_str(mocks=[input_mock])
    assert result == """\

    m: spec = create_autospec(spec=spec)"""
    input_mock.assert_not_called()


def test_generate_one_test_function():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    test.description = ''
    test.mocks = [m_mock_model]
    test.patches = []
    test.target_class_name = ''
    test.init_parameters = testscribe.namedvalues.NamedValues()
    test.parameters = testscribe.namedvalues.NamedValues()
    test.exception = None
    test.target_func_name = 'f'
    test.result = 1
    test.name = 'test1'
    m_mock_model.spec_str = 'a.Spec'
    m_mock_model.name = 'm'
    m_mock_model.attributes = {}
    m_mock_model.calls = [m_mock_call_model]
    m_mock_call_model.name = 'foo'
    m_mock_call_model.return_value = 2
    m_mock_call_model.parameters = testscribe.namedvalues.NamedValues()
    result = generate_one_test_function(test=test)
    assert result == """\
def test1():
    m: a.Spec = create_autospec(spec=a.Spec)
    m.foo.return_value = 2
    result = f()
    assert result == 1
    m_mock_calls = get_normalized_mock_calls(m, a.Spec)
    assert m_mock_calls == [
        call.foo(),
    ]
"""
    test.assert_not_called()
    m_mock_model.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_generate_result_assertion_str():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.exception = None
    test.result = 1
    result = generate_result_assertion_str(test=test)
    assert result == """\

    assert result == 1"""
    test.assert_not_called()


def test_generate_result_assertion_str_exception():
    test: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test.exception = testscribe.model_type.ExceptionModel("a.b.C", "msg")
    result = generate_result_assertion_str(test=test)
    assert result == ''
    test.assert_not_called()


def test_generate_result_assignment_str_has_exception():
    result = generate_result_assignment_str(has_exception=True)
    assert result == ''


def test_generate_result_assignment_str_no_exception():
    result = generate_result_assignment_str(has_exception=False)
    assert result == 'result = '


def test_generate_target_instance_str_class():
    result = generate_target_instance_str(target_class_name='A')
    assert result == 'instance.'


def test_generate_target_instance_str_no_class():
    result = generate_target_instance_str(target_class_name='')
    assert result == ''


def test_generate_test_str():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    all_tests.module = 'm1.m2'
    m_test_model.mocks = []
    m_test_model.exception = None
    m_test_model.result = 1
    m_test_model.init_parameters = testscribe.namedvalues.NamedValues()
    m_test_model.parameters = testscribe.namedvalues.NamedValues()
    m_test_model.patches = []
    m_test_model.target_class_name = ''
    m_test_model.target_func_name = 'f'
    m_test_model.description = ''
    m_test_model.name = 't1'
    m_test_model_1.mocks = []
    m_test_model_1.exception = None
    m_test_model_1.result = 2
    m_test_model_1.init_parameters = None
    m_test_model_1.parameters = testscribe.namedvalues.NamedValues()
    m_test_model_1.patches = []
    m_test_model_1.target_class_name = ''
    m_test_model_1.target_func_name = 'f2'
    m_test_model_1.description = ''
    m_test_model_1.name = 't2'
    result = generate_tests_output_string(all_tests=all_tests)
    assert result == """\
from m1.m2 import f, f2


def t1():
    result = f()
    assert result == 1


def t2():
    result = f2()
    assert result == 2
"""
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_generate_unit_test_file_no_test():
    m_remove_file_if_no_test: testscribe.execution_util.remove_file_if_no_test = create_autospec(spec=testscribe.execution_util.remove_file_if_no_test)
    test_file_path: pathlib.Path = create_autospec(spec=pathlib.Path)
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_remove_file_if_no_test.return_value = True
    all_tests.tests = []
    with patch('testscribe.generate_tests.remove_file_if_no_test', m_remove_file_if_no_test):
        result = generate_unit_test_file(test_file_path=test_file_path, all_tests=all_tests)
    assert result is None
    m_remove_file_if_no_test_mock_calls = get_normalized_mock_calls(m_remove_file_if_no_test, testscribe.execution_util.remove_file_if_no_test)
    assert m_remove_file_if_no_test_mock_calls == [
        call(file_path=test_file_path, tests=[]),
    ]
    test_file_path.assert_not_called()
    all_tests.assert_not_called()


def test_get_invocation_indent_level_no_patch():
    result = get_invocation_indent_level(patch_str='')
    assert result == 1


def test_get_invocation_indent_level_has_patch():
    result = get_invocation_indent_level(patch_str='fake')
    assert result == 2


def test_wrap_exception_assertion_no_exception():
    result = wrap_exception_assertion(exception_model=None, inner_statement='a\nb')
    assert result == """\
a
b"""


def test_wrap_exception_assertion():
    exception_model: testscribe.model_type.ExceptionModel = create_autospec(spec=testscribe.model_type.ExceptionModel)
    exception_model.type = 'm.c'
    exception_model.message = 'message'
    result = wrap_exception_assertion(exception_model=exception_model, inner_statement='a\nb')
    assert result == """\
with pytest.raises(m.c) as exception_info:
    a
    b
assert str(exception_info.value) == 'message'"""
    exception_model.assert_not_called()
