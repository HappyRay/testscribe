from test_data.patch_function_for_integration_test import func_with_side_effect
from test_scribe.api.mock_api import patch_with_expression, patch_with_mock


def patch_simple_int_value():
    patch_with_expression(
        target_str="test_data.simple.INT_VALUE", expression="2"
    )


def patch_func_with_side_effect():
    patch_with_mock(target=func_with_side_effect)
