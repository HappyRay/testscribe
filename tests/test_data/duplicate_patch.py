from test_data.patch_function_for_integration_test import foo, func_with_side_effect
from testscribe.api.mock_api import patch_with_mock


def duplicate_patches():
    """For integratation testing of removing duplicate patches"""
    patch_with_mock(target=func_with_side_effect)
    patch_with_mock(target=func_with_side_effect)
    patch_with_mock(target=func_with_side_effect)
    foo()
