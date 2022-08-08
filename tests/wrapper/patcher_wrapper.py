from test_scribe.api.mock_api import patch_with_expression
from test_scribe.model_type import MockNameModel
from test_scribe.patcher import remove_mock, global_var


def remove_real_mock():
    patch_with_expression(
        target_str="test_scribe.patcher.global_var.g_name_mock_dict",
        expression="{'a': 'c', 'a_1': 'd'}",
    )
    patch_with_expression(
        target_str="test_scribe.patcher.global_var.g_mock_name_counter",
        expression="collections.Counter({'a': 2})",
    )
    remove_mock(MockNameModel("a_1"))
    return global_var.g_name_mock_dict, global_var.g_mock_name_counter
