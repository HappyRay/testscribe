import test_data
from test_data.simple import C
from test_scribe import global_var
from test_scribe.api.mock_api import patch_with_mock, patch_with_expression


def test_patch_with_mock_no_effect_when_not_in_test_session():
    assert not global_var.g_test_generating_mode
    patch_with_mock("test_data.simple.C")
    assert test_data.simple.C == C


def test_patch_with_expression_no_effect_when_not_in_test_session():
    assert not global_var.g_test_generating_mode
    patch_with_expression("test_data.simple.C", 1)
    assert test_data.simple.C == C
