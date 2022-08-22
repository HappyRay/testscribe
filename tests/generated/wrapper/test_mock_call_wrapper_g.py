import test_data.simple
import testscribe.mock_call
import testscribe.namedvalues
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from wrapper.mock_call_wrapper import call_mock_call, get_call_description_wrapper


def test_call_mock_call():
    result = call_mock_call()
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] == 2
    assert isinstance(result[1], testscribe.mock_call.MockCall)
    assert result[1].method_name == 'bar'
    assert result[1].mock_name == 'mock_name'
    assert result[1].spec == test_data.simple.C
    assert result[1].previous_call_count == 0
    assert isinstance(result[1].args, testscribe.namedvalues.NamedValues)
    assert repr(result[1].args) == "NamedValues([('a', 1)])"
    assert result[1].return_value == 2


def test_get_call_description_wrapper():
    mock_call: testscribe.mock_call.MockCall = create_autospec(spec=testscribe.mock_call.MockCall)
    mock_call.args = testscribe.namedvalues.NamedValues([('a', 1)])
    mock_call.mock_name = 'f'
    mock_call.method_name = 'foo'
    result = get_call_description_wrapper(mock_call=mock_call)
    assert result == """\
f's foo method is called
with: a=1."""
    mock_call.assert_not_called()
