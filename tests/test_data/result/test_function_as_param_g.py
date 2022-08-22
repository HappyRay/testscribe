import typing
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.function_as_param import calc


def test_calc():
    m_callable: typing.Callable[[int], int] = create_autospec(spec=typing.Callable[[int], int])
    m_callable.return_value = 3
    result = calc(seed=1, f=m_callable)
    assert result == '{"result": 4}'
    m_callable_mock_calls = m_callable.mock_calls
    assert m_callable_mock_calls == [
        call(2),
    ]
