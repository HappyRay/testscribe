from __future__ import annotations

from test_data.function_as_param import calc2, calculate
from test_scribe.mocking_support import patch


def calc2_wrap(seed: int) -> int:
    patch("test_data.function_as_param.calculate", calculate)
    return calc2(seed)
