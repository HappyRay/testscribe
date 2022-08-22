import testscribe.model_type
import testscribe.namedvalues
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.model_encoder import encode_a_mock, encode_mock_calls, encode_mocks, encode_model, encode_name_and_description, encode_named_values, encode_one_mock_call, encode_one_mock_call_name, encode_one_test, encode_parameters, encode_patches, encode_result, encode_target, encode_tests


def test_encode_a_mock():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_1.name = 'm'
    m_1.spec_str = 'm1.m2'
    m_1.calls = [m_mock_call_model]
    m_1.attributes = {'a': 2}
    m_mock_call_model.name = 'c'
    m_mock_call_model.parameters = testscribe.namedvalues.NamedValues()
    m_mock_call_model.return_value = None
    result = encode_a_mock(m=m_1)
    assert result == {'name': 'm', 'spec': 'm1.m2', 'calls': [{'name': 'c', 'parameters': []}], 'attributes': {'a': 2}}
    m_1.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_encode_a_mock_no_call_no_attribute():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_1.name = 'm'
    m_1.spec_str = 'm1.m2'
    m_1.calls = []
    m_1.attributes = {}
    result = encode_a_mock(m=m_1)
    assert result == {'name': 'm', 'spec': 'm1.m2'}
    m_1.assert_not_called()


def test_encode_mock_calls():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_mock_call_model_1: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_1.calls = [m_mock_call_model, m_mock_call_model_1]
    m_mock_call_model.name = ''
    m_mock_call_model.parameters = testscribe.namedvalues.NamedValues()
    m_mock_call_model.return_value = 1
    m_mock_call_model_1.name = 'p'
    m_mock_call_model_1.parameters = testscribe.namedvalues.NamedValues()
    m_mock_call_model_1.return_value = None
    result = encode_mock_calls(m=m_1)
    assert result == [{'parameters': [], 'return': 1}, {'name': 'p', 'parameters': []}]
    m_1.assert_not_called()
    m_mock_call_model.assert_not_called()
    m_mock_call_model_1.assert_not_called()


def test_encode_mocks():
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_model_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_model.name = 'm1'
    m_mock_model.spec_str = 's1'
    m_mock_model.calls = []
    m_mock_model.attributes = {}
    m_mock_model_1.name = 'm2'
    m_mock_model_1.spec_str = 's2'
    m_mock_model_1.calls = []
    m_mock_model_1.attributes = {}
    result = encode_mocks(test={}, mocks=[m_mock_model, m_mock_model_1])
    assert result == {'mocks': [{'name': 'm1', 'spec': 's1'}, {'name': 'm2', 'spec': 's2'}]}
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()


def test_encode_mocks_no_mock():
    result = encode_mocks(test={}, mocks=[])
    assert result == {}


def test_encode_model():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model]
    all_tests.module = 'a.b'
    m_test_model.name = 't1'
    m_test_model.short_name = '_'
    m_test_model.description = ''
    m_test_model.target_func_name = 'f'
    m_test_model.target_class_name = ''
    m_test_model.init_parameters = testscribe.namedvalues.NamedValues()
    m_test_model.parameters = testscribe.namedvalues.NamedValues()
    m_test_model.exception = None
    m_test_model.result = 1
    m_test_model.patches = []
    m_test_model.mocks = []
    result = encode_model(all_tests=all_tests)
    assert result == {'format_version': 1, 'module': 'a.b', 'tests': [{'name': 't1', 'short_name': '_', 'target': {'name': 'f'}, 'parameters': [], 'result': 1}]}
    all_tests.assert_not_called()
    m_test_model.assert_not_called()


def test_encode_name_and_description_no_description():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.name = 'n'
    test_model.short_name = 's'
    test_model.description = ''
    result = encode_name_and_description(test_model=test_model)
    assert result == {'name': 'n', 'short_name': 's'}
    test_model.assert_not_called()


def test_encode_name_and_description():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.name = 'n'
    test_model.short_name = 's'
    test_model.description = 'd'
    result = encode_name_and_description(test_model=test_model)
    assert result == {'name': 'n', 'short_name': 's', 'description': 'd'}
    test_model.assert_not_called()


def test_encode_named_values():
    result = encode_named_values(values=testscribe.namedvalues.NamedValues([("", 1), ("b", 2)]))
    assert result == [{'value': 1}, {'name': 'b', 'value': 2}]


def test_encode_named_values_empty_value():
    result = encode_named_values(values=testscribe.namedvalues.NamedValues())
    assert result == []


def test_encode_one_mock_call_false_return_value_should_persist():
    result = encode_one_mock_call(mock_call=testscribe.model_type.MockCallModel(name="", parameters=testscribe.namedvalues.NamedValues(), return_value=False))
    assert result == {'parameters': [], 'return': False}


def test_encode_one_mock_call_no_name_none_return():
    result = encode_one_mock_call(mock_call=testscribe.model_type.MockCallModel(name="", parameters=testscribe.namedvalues.NamedValues(), return_value=None))
    assert result == {'parameters': []}


def test_encode_one_mock_call():
    result = encode_one_mock_call(mock_call=testscribe.model_type.MockCallModel(name="foo", parameters=testscribe.namedvalues.NamedValues([("a", 1), ("b", 2)]), return_value=3))
    assert result == {'name': 'foo', 'parameters': [{'name': 'a', 'value': 1}, {'name': 'b', 'value': 2}], 'return': 3}


def test_encode_one_mock_call_name_no_name():
    result = encode_one_mock_call_name(name='')
    assert result == {}


def test_encode_one_mock_call_name_has_name():
    result = encode_one_mock_call_name(name='a')
    assert result == {'name': 'a'}


def test_encode_one_test():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    test_model.name = 'test1'
    test_model.short_name = 'short_name'
    test_model.description = 'description'
    test_model.target_func_name = 'target_func'
    test_model.target_class_name = 'TargetClass'
    test_model.init_parameters = testscribe.namedvalues.NamedValues()
    test_model.parameters = testscribe.namedvalues.NamedValues()
    test_model.exception = None
    test_model.result = 'result'
    test_model.patches = [m_patch_model]
    test_model.mocks = [m_mock_model]
    m_patch_model.target = 'target'
    m_patch_model.replacement = 1
    m_mock_model.name = 'mock1'
    m_mock_model.spec_str = 'spec'
    m_mock_model.calls = []
    m_mock_model.attributes = {}
    result = encode_one_test(test_model=test_model)
    assert result == {'name': 'test1', 'short_name': 'short_name', 'description': 'description', 'target': {'name': 'target_func', 'class_name': 'TargetClass'}, 'parameters': [], 'result': 'result', 'patches': [{'target': 'target', 'replacement': 1}], 'mocks': [{'name': 'mock1', 'spec': 'spec'}]}
    test_model.assert_not_called()
    m_patch_model.assert_not_called()
    m_mock_model.assert_not_called()


def test_encode_parameters_no_parameter():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.init_parameters = testscribe.namedvalues.NamedValues()
    test_model.parameters = None
    result = encode_parameters(test={'foo': 1}, test_model=test_model)
    assert result == {'foo': 1}
    test_model.assert_not_called()


def test_encode_parameters_has_init_param():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.init_parameters = testscribe.namedvalues.NamedValues([("p", 1)])
    test_model.parameters = testscribe.namedvalues.NamedValues()
    result = encode_parameters(test={'foo': 1}, test_model=test_model)
    assert result == {'foo': 1, 'init_parameters': [{'name': 'p', 'value': 1}], 'parameters': []}
    test_model.assert_not_called()


def test_encode_parameters_no_init_param():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.init_parameters = testscribe.namedvalues.NamedValues()
    test_model.parameters = testscribe.namedvalues.NamedValues()
    result = encode_parameters(test={'foo': 1}, test_model=test_model)
    assert result == {'foo': 1, 'parameters': []}
    test_model.assert_not_called()


def test_encode_patches():
    m_patch_model: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_patch_model_1: testscribe.model_type.PatchModel = create_autospec(spec=testscribe.model_type.PatchModel)
    m_patch_model.target = 't1'
    m_patch_model.replacement = 1
    m_patch_model_1.target = 't2'
    m_patch_model_1.replacement = 2
    result = encode_patches(test={}, patches=[m_patch_model, m_patch_model_1])
    assert result == {'patches': [{'target': 't1', 'replacement': 1}, {'target': 't2', 'replacement': 2}]}
    m_patch_model.assert_not_called()
    m_patch_model_1.assert_not_called()


def test_encode_patches_no_patch():
    result = encode_patches(test={}, patches=[])
    assert result == {}


def test_encode_result_no_exception():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.exception = None
    test_model.result = 1
    result = encode_result(test={}, test_model=test_model)
    assert result == {'result': 1}
    test_model.assert_not_called()


def test_encode_result_exception():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.exception = testscribe.model_type.ExceptionModel("a.b.C", "msg")
    result = encode_result(test={}, test_model=test_model)
    assert result == {'exception': {'type': 'a.b.C', 'message': 'msg'}}
    test_model.assert_not_called()


def test_encode_target_no_target_class():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.target_func_name = 'f'
    test_model.target_class_name = ''
    result = encode_target(test={'foo': 1}, test_model=test_model)
    assert result == {'foo': 1, 'target': {'name': 'f'}}
    test_model.assert_not_called()


def test_encode_target():
    test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    test_model.target_func_name = 'f'
    test_model.target_class_name = 'c'
    result = encode_target(test={'foo': 1}, test_model=test_model)
    assert result == {'foo': 1, 'target': {'name': 'f', 'class_name': 'c'}}
    test_model.assert_not_called()


def test_encode_tests():
    all_tests: testscribe.model_type.AllTests = create_autospec(spec=testscribe.model_type.AllTests)
    m_test_model: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    m_test_model_1: testscribe.model_type.TestModel = create_autospec(spec=testscribe.model_type.TestModel)
    all_tests.tests = [m_test_model, m_test_model_1]
    m_test_model.name = 't1'
    m_test_model.short_name = '_'
    m_test_model.description = ''
    m_test_model.target_func_name = 'f1'
    m_test_model.target_class_name = ''
    m_test_model.init_parameters = testscribe.namedvalues.NamedValues()
    m_test_model.parameters = testscribe.namedvalues.NamedValues()
    m_test_model.exception = None
    m_test_model.result = 1
    m_test_model.patches = []
    m_test_model.mocks = []
    m_test_model_1.name = 't2'
    m_test_model_1.short_name = '_'
    m_test_model_1.description = ''
    m_test_model_1.target_func_name = 'f2'
    m_test_model_1.target_class_name = ''
    m_test_model_1.init_parameters = testscribe.namedvalues.NamedValues()
    m_test_model_1.parameters = testscribe.namedvalues.NamedValues()
    m_test_model_1.exception = None
    m_test_model_1.result = 2
    m_test_model_1.patches = []
    m_test_model_1.mocks = []
    result = encode_tests(all_tests=all_tests)
    assert result == [{'name': 't1', 'short_name': '_', 'target': {'name': 'f1'}, 'parameters': [], 'result': 1}, {'name': 't2', 'short_name': '_', 'target': {'name': 'f2'}, 'parameters': [], 'result': 2}]
    all_tests.assert_not_called()
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()
