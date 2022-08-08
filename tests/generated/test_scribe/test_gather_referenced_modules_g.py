import test_data.simple
import test_data.value
import test_scribe.model
import test_scribe.model_type
import test_scribe.namedvalues
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.gather_referenced_modules import gather_expressions, gather_expressions_from_a_mock, gather_expressions_from_mock_attributes, gather_expressions_from_mock_call_return, gather_expressions_from_mocks, gather_expressions_from_named_values, gather_expressions_from_patches, gather_import_statements_for_referenced_modules, gather_import_statements_from_module_names, gather_modules_from_expressions, get_module_names_from_expressions, get_module_names_from_value, get_module_names_in_mock_call_params, get_module_names_in_mock_specs, get_module_names_in_one_mock_call_param, get_module_names_in_result, get_referenced_modules_in_a_test


def test_gather_expressions():
    t: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_patch_model: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    t.mocks = [m_mock_model]
    t.init_parameters = test_scribe.namedvalues.NamedValues([("init", test_scribe.model_type.ExpressionModel("e"))])
    t.parameters = test_scribe.namedvalues.NamedValues([("p", test_scribe.model_type.ExpressionModel("e2"))])
    t.patches = [m_patch_model]
    m_mock_model.attributes = {"b": test_scribe.model_type.ExpressionModel("attribe2")}
    m_mock_model.calls = []
    m_patch_model.replacement = test_scribe.model_type.ExpressionModel("patch-e")
    result = gather_expressions(t=t)
    assert isinstance(result, list)
    assert len(result) == 4
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert repr(result[0]) == 'attribe2'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert repr(result[1]) == 'e'
    assert isinstance(result[2], test_scribe.model_type.ExpressionModel)
    assert repr(result[2]) == 'e2'
    assert isinstance(result[3], test_scribe.model_type.ExpressionModel)
    assert repr(result[3]) == 'patch-e'
    t.assert_not_called()
    m_mock_model.assert_not_called()
    m_patch_model.assert_not_called()


def test_gather_expressions_from_a_mock():
    m_1: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_1.attributes = {"b": test_scribe.model_type.ExpressionModel("attribe2")}
    m_1.calls = [m_mock_call_model]
    m_mock_call_model.return_value = test_scribe.model_type.ExpressionModel("e")
    result = gather_expressions_from_a_mock(m=m_1)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert repr(result[0]) == 'attribe2'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert repr(result[1]) == 'e'
    m_1.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_gather_expressions_from_mock_attributes():
    m_1: test_scribe.model.MockModel = create_autospec(spec=test_scribe.model.MockModel)
    m_1.attributes = {'a': test_scribe.model_type.ExpressionModel("attribe1"), 'b': test_scribe.model_type.ExpressionModel("attribe2")}
    result = gather_expressions_from_mock_attributes(m=m_1)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert result[0].expression == 'attribe1'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert result[1].expression == 'attribe2'
    m_1.assert_not_called()


def test_gather_expressions_from_mock_call_return():
    m_1: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_mock_call_model_1: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_mock_call_model_2: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_1.calls = [m_mock_call_model, m_mock_call_model_1, m_mock_call_model_2]
    m_mock_call_model.return_value = 1
    m_mock_call_model_1.return_value = test_scribe.model_type.ExpressionModel("e")
    m_mock_call_model_2.return_value = test_scribe.model_type.ExpressionModel("e1")
    result = gather_expressions_from_mock_call_return(m=m_1)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert repr(result[0]) == 'e'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert repr(result[1]) == 'e1'
    m_1.assert_not_called()
    m_mock_call_model.assert_not_called()
    m_mock_call_model_1.assert_not_called()
    m_mock_call_model_2.assert_not_called()


def test_gather_expressions_from_mocks():
    t: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_model_1: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    t.mocks = [m_mock_model, m_mock_model_1]
    m_mock_model.attributes = {"b": test_scribe.model_type.ExpressionModel("attribe2")}
    m_mock_model.calls = []
    m_mock_model_1.attributes = {}
    m_mock_model_1.calls = [m_mock_call_model]
    m_mock_call_model.return_value = test_scribe.model_type.ExpressionModel("e")
    result = gather_expressions_from_mocks(t=t)
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert repr(result[0]) == 'attribe2'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert repr(result[1]) == 'e'
    t.assert_not_called()
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_gather_expressions_from_named_values_none():
    result = gather_expressions_from_named_values(nv=None)
    assert result == []


def test_gather_expressions_from_named_values_has_expressions():
    result = gather_expressions_from_named_values(nv=test_scribe.namedvalues.NamedValues([('a', 1), ('b', test_scribe.model_type.ExpressionModel('e')), ('b', test_scribe.model_type.ExpressionModel('e1'))]))
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert result[0].expression == 'e'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert result[1].expression == 'e1'


def test_gather_expressions_from_named_values_no_expressions():
    result = gather_expressions_from_named_values(nv=test_scribe.namedvalues.NamedValues([('a', 1)]))
    assert result == []


def test_gather_expressions_from_patches():
    m_patch_model: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    m_patch_model_1: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    m_patch_model_2: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    m_patch_model.replacement = 1
    m_patch_model_1.replacement = test_scribe.model_type.ExpressionModel("e")
    m_patch_model_2.replacement = test_scribe.model_type.ExpressionModel("e1")
    result = gather_expressions_from_patches(patches=[m_patch_model, m_patch_model_1, m_patch_model_2])
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_scribe.model_type.ExpressionModel)
    assert repr(result[0]) == 'e'
    assert isinstance(result[1], test_scribe.model_type.ExpressionModel)
    assert repr(result[1]) == 'e1'
    m_patch_model.assert_not_called()
    m_patch_model_1.assert_not_called()
    m_patch_model_2.assert_not_called()


def test_gather_import_statements_for_referenced_modules():
    m_test_model: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model_1: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_test_model.mocks = []
    m_test_model.exception = None
    m_test_model.result = test_scribe.model_type.CallableModel("foo", "call_mod")
    m_test_model.init_parameters = test_scribe.namedvalues.NamedValues()
    m_test_model.parameters = test_scribe.namedvalues.NamedValues()
    m_test_model.patches = []
    m_test_model_1.mocks = []
    m_test_model_1.exception = test_scribe.model_type.ExceptionModel("a.b.C", "msg")
    m_test_model_1.init_parameters = test_scribe.namedvalues.NamedValues()
    m_test_model_1.parameters = test_scribe.namedvalues.NamedValues()
    m_test_model_1.patches = []
    result = gather_import_statements_for_referenced_modules(tests=[m_test_model, m_test_model_1])
    assert result == ['import a.b', 'import call_mod']
    m_test_model.assert_not_called()
    m_test_model_1.assert_not_called()


def test_gather_import_statements_from_module_names_normal():
    result = gather_import_statements_from_module_names(module_names=['a.b', 'c'])
    assert result == ['import a.b', 'import c']


def test_gather_import_statements_from_module_names_ignore_builtins():
    result = gather_import_statements_from_module_names(module_names=['builtins'])
    assert result == []


def test_gather_modules_from_expressions():
    m_expression_model: test_scribe.model_type.ExpressionModel = create_autospec(spec=test_scribe.model_type.ExpressionModel)
    m_expression_model_1: test_scribe.model_type.ExpressionModel = create_autospec(spec=test_scribe.model_type.ExpressionModel)
    m_expression_model_2: test_scribe.model_type.ExpressionModel = create_autospec(spec=test_scribe.model_type.ExpressionModel)
    m_expression_model.expression = '1'
    m_expression_model_1.expression = 'test_data.simple.C'
    m_expression_model_2.expression = 'test_data.simple.C'
    result = gather_modules_from_expressions(expressions=[m_expression_model, m_expression_model_1, m_expression_model_2])
    assert result == ['test_data.simple', 'test_data.simple']
    m_expression_model.assert_not_called()
    m_expression_model_1.assert_not_called()
    m_expression_model_2.assert_not_called()


def test_get_module_names_from_expressions():
    t: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    t.mocks = []
    t.init_parameters = test_scribe.namedvalues.NamedValues()
    t.parameters = test_scribe.namedvalues.NamedValues([("p", test_scribe.model_type.ExpressionModel("test_data.simple.C"))])
    t.patches = []
    result = get_module_names_from_expressions(t=t)
    assert result == ['test_data.simple']
    t.assert_not_called()


def test_get_module_names_from_value_dict():
    result = get_module_names_from_value(v={"a": 1, "b": test_scribe.model_type.CallableModel("foo", "a"), test_data.value.object_model_c: 2})
    assert result == ['a', 'test_data.simple']


def test_get_module_names_from_value_set():
    result = get_module_names_from_value(v={test_scribe.model_type.CallableModel("foo", "a")})
    assert result == ['a']


def test_get_module_names_from_value_tuple():
    result = get_module_names_from_value(v=(1, test_scribe.model_type.CallableModel("foo", "a")))
    assert result == ['a']


def test_get_module_names_from_value_list():
    result = get_module_names_from_value(v=[test_scribe.model_type.CallableModel("foo", "a"), 1])
    assert result == ['a']


def test_get_module_names_from_value_callable_model():
    result = get_module_names_from_value(v=test_scribe.model_type.CallableModel("foo", "a"))
    assert result == ['a']


def test_get_module_names_from_value_object_model_with_object_model_member():
    result = get_module_names_from_value(v=test_scribe.model_type.ObjectModel(type="a.B", repr="", members={"m": 1, "m2": test_scribe.model_type.ObjectModel("c.D", "", {})}))
    assert result == ['a', 'c']


def test_get_module_names_in_mock_call_params():
    t: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_model_1: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    m_mock_call_model_1: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    t.mocks = [m_mock_model, m_mock_model_1]
    m_mock_model.calls = [m_mock_call_model]
    m_mock_model_1.calls = [m_mock_call_model_1]
    m_mock_call_model.parameters = test_scribe.namedvalues.NamedValues([("a", test_data.value.callable_model_foo)])
    m_mock_call_model_1.parameters = test_scribe.namedvalues.NamedValues([("b", test_data.value.object_model_c)])
    result = get_module_names_in_mock_call_params(t=t)
    assert result == ['test_data.simple', 'test_data.simple']
    t.assert_not_called()
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()
    m_mock_call_model.assert_not_called()
    m_mock_call_model_1.assert_not_called()


def test_get_module_names_in_mock_specs():
    test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_model_1: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    test.mocks = [m_mock_model, m_mock_model_1]
    m_mock_model.spec_str = 'a.B'
    m_mock_model_1.spec_str = 'c.D'
    result = get_module_names_in_mock_specs(test=test)
    assert result == ['a', 'c']
    test.assert_not_called()
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()


def test_get_module_names_in_one_mock_call_param():
    result = get_module_names_in_one_mock_call_param(params=test_scribe.namedvalues.NamedValues([("a", test_data.value.callable_model_foo), ("b", test_data.value.object_model_c)]))
    assert result == ['test_data.simple', 'test_data.simple']


def test_get_module_names_in_result_normal():
    test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    test.exception = None
    test.result = test_scribe.model_type.CallableModel("foo", "a")
    result = get_module_names_in_result(test=test)
    assert result == ['a']
    test.assert_not_called()


def test_get_module_names_in_result_exception():
    test: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    test.exception = test_scribe.model_type.ExceptionModel("a.b.C", "msg")
    result = get_module_names_in_result(test=test)
    assert result == ['a.b']
    test.assert_not_called()


def test_get_referenced_modules_in_a_test():
    t: test_scribe.model_type.TestModel = create_autospec(spec=test_scribe.model_type.TestModel)
    m_mock_model: test_scribe.model_type.MockModel = create_autospec(spec=test_scribe.model_type.MockModel)
    m_mock_call_model: test_scribe.model_type.MockCallModel = create_autospec(spec=test_scribe.model_type.MockCallModel)
    t.mocks = [m_mock_model]
    t.exception = test_scribe.model_type.ExceptionModel("a.b.C", "msg")
    t.init_parameters = test_scribe.namedvalues.NamedValues()
    t.parameters = test_scribe.namedvalues.NamedValues([("p", test_scribe.model_type.ExpressionModel("test_data.simple.C"))])
    t.patches = []
    m_mock_model.spec_str = 'spec_mod.A'
    m_mock_model.calls = [m_mock_call_model]
    m_mock_model.attributes = {}
    m_mock_call_model.parameters = test_scribe.namedvalues.NamedValues([("p", test_scribe.model_type.CallableModel("foo", "call_mod"))])
    m_mock_call_model.return_value = 1
    result = get_referenced_modules_in_a_test(t=t)
    assert result == ['spec_mod', 'call_mod', 'a.b', 'test_data.simple']
    t.assert_not_called()
    m_mock_model.assert_not_called()
    m_mock_call_model.assert_not_called()
