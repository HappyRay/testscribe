from typing import Any

from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data.simple import C
from test_scribe.api.mock_api import patch_with_mock
from test_scribe.eval_expression import (
    contain_mock_proxy,
    process_mock_marker,
    wrap_input_value,
    process_complex_value,
)
from test_scribe.mock_proxy import MockProxy
from test_scribe.value_util import InputValue


def contain_mock_proxy_wrapper():
    m = create_mock_proxy_for_c()
    return contain_mock_proxy({"a": m})


def process_complex_value_wrapper_mixed_m_function_complex_obj():
    m = create_mock_proxy_for_c()
    v = (m, C(1))
    # can't use generated assertion for the returned tuple directly
    # since the mock object will not be created in the generated code.
    m_return, c = process_complex_value(
        value=v, expression="(m(test_data.simple.C), test_data.simple.C(1))"
    )
    assert m_return == m
    return c


def create_mock_proxy_for_c():
    patch_globals_modified_by_mock_proxy()
    # has to explictly create MockProxy
    # if it is created via a parameter, in the generated test a MagicMock object
    # will be returned instead.
    return MockProxy(spec=C, name="m_c")


def wrap_input_value_wrapper_complex_value(value: Any):
    """
    The input has to be a "complex" expression.
    The return value is an InputValue which is translated to its expression only
    Thus, it has to be treated differently here.
    """
    expression = "foo"
    r = wrap_input_value(v=value, expression=expression)
    assert isinstance(r, InputValue)
    assert r.expression == expression
    return r.value


def process_mock_marker_wrapper(t: type, v: Any):
    # This function creates a MockProxy internally.
    # The normal generated test function will compare the result with a mock object
    # created outside this function, which will fail.
    # Intercept the MockProxy creation call allows us to verify the behavior
    # Return a simple value instead of a real MockProxy when MockProxy is created
    # to make it easier to verify the result since MockProxy is a special type.

    # Use the setup function to mock MockProxy interferes with the tool itself
    # since the setup function is called before the tool references MockProxy.
    #
    patch_with_mock(target="test_scribe.eval_expression.MockProxy")
    return process_mock_marker(t=t, v=v)
