import fixture.helper
import pathlib
import testscribe.model_type
import testscribe.namedvalues
import pytest
from testscribe.load_scribe_file import get_named_value_element_value, load_exception_internal, load_exception_model, load_mock_attributes, load_mock_call_model, load_mock_calls, load_mock_model, load_mocks, load_model, load_named_values, load_one_patch, load_optional_name_key_value, load_or_create_model, load_patches, load_required_name_key_value, load_result, load_scribe_file, load_short_name, load_target, load_target_class_name, load_test, load_test_description


def test_get_named_value_element_value_value_key_is_required():
    with pytest.raises(KeyError) as exception_info:
        get_named_value_element_value(d={})
    assert "'value'" == str(exception_info.value)


def test_get_named_value_element_value():
    result = get_named_value_element_value(d={'value': 1})
    assert result == 1


def test_load_exception_internal():
    result = load_exception_internal(d={'type': 'a', 'message': 'b'})
    assert isinstance(result, testscribe.model_type.ExceptionModel)
    assert repr(result) == "ExceptionModel(type='a', message='b')"


def test_load_exception_internal_type_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_exception_internal(d={})
    assert "'type'" == str(exception_info.value)


def test_load_exception_internal_message_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_exception_internal(d={'type': 'a'})
    assert "'message'" == str(exception_info.value)


def test_load_exception_model():
    result = load_exception_model(d={'exception': {'type': 'a', 'message': 'b'}})
    assert isinstance(result, testscribe.model_type.ExceptionModel)
    assert repr(result) == "ExceptionModel(type='a', message='b')"


def test_load_exception_model_no_exception():
    result = load_exception_model(d={})
    assert result is None


def test_load_mock_attributes_no_attribute():
    result = load_mock_attributes(m={})
    assert result == {}


def test_load_mock_attributes_has_attribute():
    result = load_mock_attributes(m={'attributes': {'a': 1}})
    assert result == {'a': 1}


def test_load_mock_call_model_default():
    result = load_mock_call_model(c={})
    assert isinstance(result, testscribe.model_type.MockCallModel)
    assert repr(result) == "MockCallModel(name='', parameters=NamedValues([]), return_value=None)"


def test_load_mock_call_model():
    result = load_mock_call_model(c={'name': 'n', 'parameters': [{'name': 'a', 'value': 1}], 'return': 3})
    assert isinstance(result, testscribe.model_type.MockCallModel)
    assert repr(result) == "MockCallModel(name='n', parameters=NamedValues([('a', 1)]), return_value=3)"


def test_load_mock_calls_has_call():
    result = load_mock_calls(m={'calls': [{'name': 'n', 'parameters': [{'name': 'a', 'value': 1}], 'return': 3}, {}]})
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], testscribe.model_type.MockCallModel)
    assert repr(result[0]) == "MockCallModel(name='n', parameters=NamedValues([('a', 1)]), return_value=3)"
    assert isinstance(result[1], testscribe.model_type.MockCallModel)
    assert repr(result[1]) == "MockCallModel(name='', parameters=NamedValues([]), return_value=None)"


def test_load_mock_calls_no_call():
    result = load_mock_calls(m={})
    assert result == []


def test_load_mock_model_name_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_mock_model(m={})
    assert "'name'" == str(exception_info.value)


def test_load_mock_model_spec_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_mock_model(m={'name': 'm'})
    assert "'spec'" == str(exception_info.value)


def test_load_mock_model():
    result = load_mock_model(m={'name': 'm', 'spec': 's'})
    assert isinstance(result, testscribe.model_type.MockModel)
    assert repr(result) == "MockModel(name='m', spec_str='s', calls=[], attributes={})"


def test_load_mocks():
    result = load_mocks(d={'mocks': [{'name': 'm', 'spec': 's'}, {'name': 'm1', 'spec': 's1'}]})
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], testscribe.model_type.MockModel)
    assert repr(result[0]) == "MockModel(name='m', spec_str='s', calls=[], attributes={})"
    assert isinstance(result[1], testscribe.model_type.MockModel)
    assert repr(result[1]) == "MockModel(name='m1', spec_str='s1', calls=[], attributes={})"


def test_load_mocks_no_mock():
    result = load_mocks(d={})
    assert result == []


def test_load_model():
    result = load_model(d={'module': 'mod', 'tests': [{'name': 't', 'short_name': 'st', 'target': {'name': 'f'}}, {'name': 't1', 'short_name': 'st1', 'target': {'name': 'f1'}}]})
    assert isinstance(result, testscribe.model_type.AllTests)
    assert repr(result) == "AllTests(tests=[TestModel(name='t', short_name='st', description='', target_func_name='f', target_class_name='', init_parameters=NamedValues([]), parameters=NamedValues([]), exception=None, result=None, mocks=[], patches=[]), TestModel(name='t1', short_name='st1', description='', target_func_name='f1', target_class_name='', init_parameters=NamedValues([]), parameters=NamedValues([]), exception=None, result=None, mocks=[], patches=[])], module='mod', name_to_index={'t': 0, 't1': 1})"


def test_load_named_values_missing_key():
    result = load_named_values(d={}, key_name='k')
    assert isinstance(result, testscribe.namedvalues.NamedValues)
    assert repr(result) == 'NamedValues([])'


def test_load_named_values():
    result = load_named_values(d={'k': [{'value': 1}, {'name': 'b', 'value': 2}]}, key_name='k')
    assert isinstance(result, testscribe.namedvalues.NamedValues)
    assert repr(result) == "NamedValues([('', 1), ('b', 2)])"


def test_load_one_patch_target_key_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_one_patch(d={})
    assert "'target'" == str(exception_info.value)


def test_load_one_patch_replacement_key_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_one_patch(d={'target': 'a'})
    assert "'replacement'" == str(exception_info.value)


def test_load_one_patch():
    result = load_one_patch(d={'target': 'a', 'replacement': 1})
    assert isinstance(result, testscribe.model_type.PatchModel)
    assert repr(result) == "PatchModel(target='a', replacement=1)"


def test_load_optional_name_key_value_no_key():
    result = load_optional_name_key_value(d={})
    assert result == ''


def test_load_optional_name_key_value_has_key():
    result = load_optional_name_key_value(d={'name': 'a'})
    assert result == 'a'


def test_load_or_create_model_non_existing_file():
    result = load_or_create_model(file_path=pathlib.Path("foo"), full_module_name='a.b')
    assert isinstance(result, testscribe.model_type.AllTests)
    assert repr(result) == "AllTests(tests=[], module='a.b', name_to_index={})"


def test_load_or_create_model_existing_file():
    result = load_or_create_model(file_path=fixture.helper.get_test_result_path().joinpath("service_call.tscribe"), full_module_name='a.b')
    assert isinstance(result, testscribe.model_type.AllTests)
    assert repr(result) == 'AllTests(tests=[TestModel(name=\'test_simple_gen\', short_name=\'simple_gen\', description=\'integration test\', target_func_name=\'gen_name\', target_class_name=\'\', init_parameters=NamedValues([]), parameters=NamedValues([(\'service\', m_service), (\'keyword\', \'a\'), (\'start_number\', 1)]), exception=None, result=\'{"name": "b", "number": 5}\', mocks=[MockModel(name=\'m_service\', spec_str=\'test_data.service.Service\', calls=[MockCallModel(name=\'search_a_name\', parameters=NamedValues([(\'keyword\', \'key: a\')]), return_value=\'b\'), MockCallModel(name=\'search_a_number\', parameters=NamedValues([(\'seed_number\', 1)]), return_value=2), MockCallModel(name=\'search_a_number\', parameters=NamedValues([(\'seed_number\', 2)]), return_value=3)], attributes={})], patches=[])], module=\'test_data.service_call\', name_to_index={\'test_simple_gen\': 0})'


def test_load_patches():
    result = load_patches(d={'patches': [{'target': 'a', 'replacement': 1}, {'target': 'b', 'replacement': 2}]})
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], testscribe.model_type.PatchModel)
    assert repr(result[0]) == "PatchModel(target='a', replacement=1)"
    assert isinstance(result[1], testscribe.model_type.PatchModel)
    assert repr(result[1]) == "PatchModel(target='b', replacement=2)"


def test_load_patches_no_patch():
    result = load_patches(d={})
    assert result == []


def test_load_required_name_key_value_name_key_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_required_name_key_value(d={})
    assert "'name'" == str(exception_info.value)


def test_load_required_name_key_value():
    result = load_required_name_key_value(d={'name': 'a'})
    assert result == 'a'


def test_load_result():
    result = load_result(d={'result': 1})
    assert result == 1


def test_load_result_default():
    result = load_result(d={})
    assert result is None


def test_load_scribe_file():
    result = load_scribe_file(scribe_file=fixture.helper.get_test_data_root_path().joinpath("result").joinpath("service_call.tscribe"))
    assert isinstance(result, testscribe.model_type.AllTests)
    assert repr(result) == 'AllTests(tests=[TestModel(name=\'test_simple_gen\', short_name=\'simple_gen\', description=\'integration test\', target_func_name=\'gen_name\', target_class_name=\'\', init_parameters=NamedValues([]), parameters=NamedValues([(\'service\', m_service), (\'keyword\', \'a\'), (\'start_number\', 1)]), exception=None, result=\'{"name": "b", "number": 5}\', mocks=[MockModel(name=\'m_service\', spec_str=\'test_data.service.Service\', calls=[MockCallModel(name=\'search_a_name\', parameters=NamedValues([(\'keyword\', \'key: a\')]), return_value=\'b\'), MockCallModel(name=\'search_a_number\', parameters=NamedValues([(\'seed_number\', 1)]), return_value=2), MockCallModel(name=\'search_a_number\', parameters=NamedValues([(\'seed_number\', 2)]), return_value=3)], attributes={})], patches=[])], module=\'test_data.service_call\', name_to_index={\'test_simple_gen\': 0})'


def test_load_short_name():
    result = load_short_name(d={'short_name': 'a'})
    assert result == 'a'


def test_load_short_name_short_name_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_short_name(d={})
    assert "'short_name'" == str(exception_info.value)


def test_load_target_target_key_is_required():
    with pytest.raises(KeyError) as exception_info:
        load_target(d={})
    assert "'target'" == str(exception_info.value)


def test_load_target():
    result = load_target(d={'target': {'name': 'a', 'class_name': 'c'}})
    assert result == ('a', 'c')


def test_load_target_class_name_no_class():
    result = load_target_class_name(d={})
    assert result == ''


def test_load_target_class_name_has_class():
    result = load_target_class_name(d={'class_name': 'a'})
    assert result == 'a'


def test_load_test():
    result = load_test(d={'name': 'a', 'short_name': 'b', 'target': {'name': 'c'}, 'init_parameters': [{'name': 'p', 'value': 1}], 'parameters': [{'value': 2}]})
    assert isinstance(result, testscribe.model_type.TestModel)
    assert repr(result) == "TestModel(name='a', short_name='b', description='', target_func_name='c', target_class_name='', init_parameters=NamedValues([('p', 1)]), parameters=NamedValues([('', 2)]), exception=None, result=None, mocks=[], patches=[])"


def test_load_test_description_default():
    result = load_test_description(d={})
    assert result == ''


def test_load_test_description_has_description():
    result = load_test_description(d={'description': 'a'})
    assert result == 'a'
