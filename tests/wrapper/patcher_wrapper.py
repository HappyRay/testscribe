from testscribe.api.mock_api import patch_with_expression
from testscribe.model_type import MockNameModel
from testscribe.patcher import remove_mock, global_var


def remove_real_mock():
    patch_with_expression(
        target_str="testscribe.patcher.global_var.g_name_mock_dict",
        expression="{'a': 'c', 'a_1': 'd'}",
    )
    patch_with_expression(
        target_str="testscribe.patcher.global_var.g_mock_name_counter",
        expression="collections.Counter({'a': 2})",
    )
    remove_mock(MockNameModel("a_1"))
    return global_var.g_name_mock_dict, global_var.g_mock_name_counter
