import test_data.patch_function_for_integration_test
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from test_data.patch_function_for_integration_test import foo


def test_foo():
    m_func_with_side_effect: test_data.patch_function_for_integration_test.func_with_side_effect = create_autospec(spec=test_data.patch_function_for_integration_test.func_with_side_effect)
    m_func_with_side_effect.return_value = None
    with patch('test_data.patch_function_for_integration_test.func_with_side_effect', m_func_with_side_effect):
        result = foo()
    assert result is None
    m_func_with_side_effect_mock_calls = get_normalized_mock_calls(m_func_with_side_effect, test_data.patch_function_for_integration_test.func_with_side_effect)
    assert m_func_with_side_effect_mock_calls == [
        call(),
    ]
