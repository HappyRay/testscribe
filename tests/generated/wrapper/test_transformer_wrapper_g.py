import collections
import test_scribe.global_var
import test_scribe.model_type
from unittest.mock import patch
from wrapper.transformer_wrapper import tranform_module, transform_mock_proxy


def test_tranform_module():
    result = tranform_module()
    assert isinstance(result, test_scribe.model_type.ModuleModel)
    assert repr(result) == "ModuleModel(name='test_data.simple')"


def test_transform_mock_proxy():
    with patch('test_scribe.global_var.g_mock_name_counter', collections.Counter(test_scribe.global_var.g_mock_name_counter)), patch('test_scribe.global_var.g_name_mock_dict', {}):
        result = transform_mock_proxy()
    assert isinstance(result, test_scribe.model_type.MockNameModel)
    assert repr(result) == 'a'
