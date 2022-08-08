from typing import Any

from test_scribe.gen_patch_code import generate_patch_str
from test_scribe.model import create_patch_model
from test_scribe.patcher import create_patcher


def patch_common_code_gen(value: Any):
    """
    Patch with a primitiave value should generate correct patch code.

    Create this wrapper function to mimic the prodution logic
    to avoid the complication of testing the production logic directly.
    e.g. clear the global variable g_patchers and actually starting and stopping
    patches.
    :return:
    """
    p = create_patcher(target_str="t", instance=None, replacement=value)
    p_model = create_patch_model(p)
    return generate_patch_str([p_model])
