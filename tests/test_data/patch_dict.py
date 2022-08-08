from test_scribe.api.mock_api import patch_with_expression

a_dict = {"a": 1}


def get_patched_dict():
    patch_with_expression(
        target_str="test_data.patch_dict.a_dict", expression='{"b": 1 + 1}'
    )
    return a_dict
