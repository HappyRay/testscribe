from typing import List

from testscribe.config import g_indent
from testscribe.model_type import PatchModel


def generate_patch_str(patches: List[PatchModel]) -> str:
    if not patches:
        return ""
    patch_str_list = [f"patch('{p.target}', {repr(p.replacement)})" for p in patches]
    patch_str = ", ".join(patch_str_list)
    return f"\n{g_indent}with {patch_str}:"
