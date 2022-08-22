import test_data.value
import testscribe.gen_mock_verification_code
import testscribe.model_type
import testscribe.namedvalues
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from testscribe.gen_mock_verification_code import generate_complex_param_verification, generate_mock_call_list, generate_mock_call_list_verfication, generate_mock_call_verification, generate_mock_call_verification_str, generate_one_call_str, generate_one_mock_call, get_mock_call_params, get_mock_calls_variable_value, get_one_complex_param, get_one_mock_call_arg_str, get_one_mock_call_param, update_complex_mock_call_arg_map


def test_generate_complex_param_verification():
    params: testscribe.gen_mock_verification_code.ComplexMockCallParam = create_autospec(spec=testscribe.gen_mock_verification_code.ComplexMockCallParam)
    params.index = 2
    params.name_to_value = {'p': 1, 'p2': 2}
    params.index_to_value = {3: True, 5: 'a'}
    result = generate_complex_param_verification(params=params, mock_calls_name='v')
    assert result == ["    assert v[2].kwargs['p'] == 1", "    assert v[2].kwargs['p2'] == 2", '    assert v[2].args[3] is True', "    assert v[2].args[5] == 'a'"]
    params.assert_not_called()


def test_generate_mock_call_list_no_call():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_1.calls = []
    result = generate_mock_call_list(m=m_1)
    assert isinstance(result, testscribe.gen_mock_verification_code.MockCallList)
    assert repr(result) == "MockCallList(call_list_str='', complex_params=[])"
    m_1.assert_not_called()


def test_generate_mock_call_list_two_method_calls_one_with_complex_param():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_mock_call_model_1: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_1.calls = [m_mock_call_model, m_mock_call_model_1]
    m_mock_call_model.parameters = testscribe.namedvalues.NamedValues([("p", 1)])
    m_mock_call_model.name = 'm1'
    m_mock_call_model_1.parameters = testscribe.namedvalues.NamedValues([("p2", testscribe.model_type.ObjectModel("t", "r", {}))])
    m_mock_call_model_1.name = 'm2'
    result = generate_mock_call_list(m=m_1)
    assert isinstance(result, testscribe.gen_mock_verification_code.MockCallList)
    assert repr(result) == "MockCallList(call_list_str='call.m1(p=1),\\ncall.m2(p2=ANY),', complex_params=[ComplexMockCallParam(index=1, name_to_value={'p2': r}, index_to_value={})])"
    m_1.assert_not_called()
    m_mock_call_model.assert_not_called()
    m_mock_call_model_1.assert_not_called()


def test_generate_mock_call_list_verfication():
    result = generate_mock_call_list_verfication(mock_name='m', spec_str='testscribe.simple.C', mock_calls_name='v', call_list_str='call list str')
    assert result == """\
    v = get_normalized_mock_calls(m, testscribe.simple.C)
    assert v == [
        call list str
    ]"""


def test_generate_mock_call_verification_no_call():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_1.calls = []
    m_1.name = 'm'
    result = generate_mock_call_verification(m=m_1)
    assert result == '    m.assert_not_called()'
    m_1.assert_not_called()


def test_generate_mock_call_verification():
    m_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_1.calls = [m_mock_call_model]
    m_1.spec_str = 'spec_str'
    m_1.name = 'm'
    m_mock_call_model.parameters = testscribe.namedvalues.NamedValues([('p', test_data.value.object_model_c)])
    m_mock_call_model.name = 'c'
    result = generate_mock_call_verification(m=m_1)
    assert result == """\
    m_mock_calls = get_normalized_mock_calls(m, spec_str)
    assert m_mock_calls == [
        call.c(p=ANY),
    ]
    assert isinstance(m_mock_calls[0].kwargs['p'], test_data.simple.C)
    assert m_mock_calls[0].kwargs['p'].a == 1"""
    m_1.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_generate_mock_call_verification_statements():
    m_mock_model: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_model_1: testscribe.model_type.MockModel = create_autospec(spec=testscribe.model_type.MockModel)
    m_mock_call_model: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    m_mock_model.calls = []
    m_mock_model.name = 'm'
    m_mock_model_1.calls = [m_mock_call_model]
    m_mock_model_1.spec_str = 'spec_str'
    m_mock_model_1.name = 'm1'
    m_mock_call_model.parameters = testscribe.namedvalues.NamedValues()
    m_mock_call_model.name = 'c'
    result = generate_mock_call_verification_str(mocks=[m_mock_model, m_mock_model_1])
    assert result == """\

    m.assert_not_called()
    m1_mock_calls = get_normalized_mock_calls(m1, spec_str)
    assert m1_mock_calls == [
        call.c(),
    ]"""
    m_mock_model.assert_not_called()
    m_mock_model_1.assert_not_called()
    m_mock_call_model.assert_not_called()


def test_generate_one_call_str_method():
    result = generate_one_call_str(method_name='m', param_str='p')
    assert result == 'call.m(p),'


def test_generate_one_call_str_direct_call():
    result = generate_one_call_str(method_name='', param_str='p')
    assert result == 'call(p),'


def test_generate_one_mock_call_method_call_with_simple_named_param():
    call: testscribe.model_type.MockCallModel = create_autospec(spec=testscribe.model_type.MockCallModel)
    call.parameters = testscribe.namedvalues.NamedValues([("p", 2)])
    call.name = 'm'
    result = generate_one_mock_call(index=1, call=call)
    assert result == ('call.m(p=2),', None)
    call.assert_not_called()


def test_get_mock_call_params():
    result = get_mock_call_params(param_list=[("", 1), ("p", test_data.value.object_model_d)])
    assert isinstance(result, testscribe.gen_mock_verification_code.MockCallParams)
    assert repr(result) == "MockCallParams(param_str='1, p=ANY', name_to_value={'p': test_data.simple.ReadOnlyData(a=1)}, index_to_value={})"


def test_get_mock_calls_variable_value_has_param_info():
    result = get_mock_calls_variable_value(mock_name='m', spec_str='testscribe.simple.C')
    assert result == 'get_normalized_mock_calls(m, testscribe.simple.C)'


def test_get_mock_calls_variable_value_no_param_info():
    result = get_mock_calls_variable_value(mock_name='m', spec_str='typing.Callable')
    assert result == 'm.mock_calls'


def test_get_one_complex_param_no_complex_param():
    call_params: testscribe.gen_mock_verification_code.MockCallParams = create_autospec(spec=testscribe.gen_mock_verification_code.MockCallParams)
    call_params.name_to_value = {}
    call_params.index_to_value = {}
    result = get_one_complex_param(call_params=call_params, index=1)
    assert result is None
    call_params.assert_not_called()


def test_get_one_complex_param_named_complex_param():
    call_params: testscribe.gen_mock_verification_code.MockCallParams = create_autospec(spec=testscribe.gen_mock_verification_code.MockCallParams)
    call_params.name_to_value = {'p': 1}
    call_params.index_to_value = {}
    result = get_one_complex_param(call_params=call_params, index=1)
    assert isinstance(result, testscribe.gen_mock_verification_code.ComplexMockCallParam)
    assert repr(result) == "ComplexMockCallParam(index=1, name_to_value={'p': 1}, index_to_value={})"
    call_params.assert_not_called()


def test_get_one_complex_param_unnamed_complex_param():
    """
    For simplicity of this test the complex param value is represented by a simple value
    """
    call_params: testscribe.gen_mock_verification_code.MockCallParams = create_autospec(spec=testscribe.gen_mock_verification_code.MockCallParams)
    call_params.name_to_value = {}
    call_params.index_to_value = {2: True}
    result = get_one_complex_param(call_params=call_params, index=1)
    assert isinstance(result, testscribe.gen_mock_verification_code.ComplexMockCallParam)
    assert repr(result) == 'ComplexMockCallParam(index=1, name_to_value={}, index_to_value={2: True})'
    call_params.assert_not_called()


def test_get_one_mock_call_arg_str_no_param_name():
    result = get_one_mock_call_arg_str(value_str='v', param_name='')
    assert result == 'v'


def test_get_one_mock_call_arg_str_with_param_name():
    result = get_one_mock_call_arg_str(value_str='v', param_name='p')
    assert result == 'p=v'


def test_get_one_mock_call_param_regular_value():
    result = get_one_mock_call_param(arg_list=[], name_to_value={}, index_to_value={}, index=0, param_name='p', v=1)
    assert result == (['p=1'], {}, {})


def test_get_one_mock_call_param_complex_param():
    result = get_one_mock_call_param(arg_list=[], name_to_value={}, index_to_value={}, index=0, param_name='', v=test_data.value.object_model_d)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert result[0] == ['ANY']
    assert result[1] == {}
    assert isinstance(result[2], dict)
    assert len(result[2]) == 1
    assert isinstance(result[2][0], testscribe.model_type.ObjectModel)
    assert repr(result[2][0]) == 'test_data.simple.ReadOnlyData(a=1)'


def test_update_complex_mock_call_arg_map_with_param_name():
    result = update_complex_mock_call_arg_map(name_to_value={}, index_to_value={}, index=0, param_name='p', v=1)
    assert result == ({'p': 1}, {})


def test_update_complex_mock_call_arg_map_no_param_name():
    result = update_complex_mock_call_arg_map(name_to_value={}, index_to_value={}, index=0, param_name='', v=1)
    assert result == ({}, {0: 1})
