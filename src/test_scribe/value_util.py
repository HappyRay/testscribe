from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def get_value_repr(v) -> str:
    from test_scribe.mock_proxy import MockProxy, get_proxy_str

    if isinstance(v, InputValue):
        return v.expression
    if isinstance(v, MockProxy):
        return get_proxy_str(v)
    return repr(v)


def get_value(v):
    if isinstance(v, InputValue):
        return v.value
    return v


@dataclass
class InputValue:
    """
    Encapsulate a value that is derived from an expression
    and the expression needs to be preserved to generate the correct
    test code.
    e.g.
    test_data.simple.C(1)
    ignore
    throw(Exception("err"))
    generate_data(1) generate_data is a user defined function
    that returns some complex values such as class instances.

    """

    # an expression to generate the value
    expression: str
    value: Any
