from unittest.mock import patch, Mock, call

from test_data.simple import foo, C
from testscribe.context import Context
from testscribe.mock_call import MockCall
from testscribe.special_type import NoDefault


# The MockCall function is used by the tool itself
# Patching these calls using the tool will result in recursive calls.
# Thus, these tests have to be written manually.
@patch("testscribe.mock_call.log", autospec=True)
@patch("testscribe.mock_call.show_user_call_stack", autospec=True)
@patch("testscribe.value_input.get_one_value", autospec=True)
def test_call_mock_function(
    mock_get_one_value: Mock, mock_show_user_call_stack: Mock, mock_log: Mock
):
    mock_get_one_value.return_value = 0
    m = MockCall(method_name="", spec=foo, mock_name="m_foo", previous_call_count=0)
    r = m(1)
    assert r == 0
    description = "m_foo is called\nwith: a=1."
    mock_log.mock_calls == [  # noqa
        call(description),
        call("Mock call return value: 0"),
    ]
    mock_show_user_call_stack.assert_called_once()
    mock_get_one_value.assert_called_once_with(
        prompt_name="the return value",
        t=int,
        context=Context(description),
        default=NoDefault,
    )
    assert m.args.params == [("a", 1)]
    assert m.return_value == 0


@patch("testscribe.mock_call.log", autospec=True)
@patch("testscribe.mock_call.show_user_call_stack", autospec=True)
@patch("testscribe.value_input.get_one_value", autospec=True)
def test_call_mock_method_with_class(
    mock_get_one_value: Mock, mock_show_user_call_stack: Mock, mock_log: Mock
):
    mock_get_one_value.return_value = 2
    m = MockCall(method_name="", spec=C, mock_name="m_c", previous_call_count=0)
    r = m(1)
    assert r == 2
    description = "m_c is called\nwith: a=1."
    mock_log.assert_any_call(description)
    mock_show_user_call_stack.assert_called_once()
    mock_get_one_value.assert_called_once_with(
        prompt_name="the return value",
        t=C,
        context=Context(description),
        default=NoDefault,
    )
    assert m.args.params == [("a", 1)]
    assert m.return_value == 2


@patch("testscribe.mock_call.log", autospec=True)
@patch("testscribe.mock_call.show_user_call_stack", autospec=True)
@patch("testscribe.value_input.get_one_value", autospec=True)
def test_call_mock_method(
    mock_get_one_value: Mock, mock_show_user_call_stack: Mock, mock_log: Mock
):
    mock_get_one_value.return_value = 0
    m = MockCall(method_name="bar", spec=C, mock_name="m_c", previous_call_count=0)
    r = m(1)
    assert r == 0
    description = "m_c's bar method is called\nwith: a=1."
    mock_log.mock_calls = [call(description), call("Mock call return value: 0")]
    mock_show_user_call_stack.assert_called_once()
    mock_get_one_value.assert_called_once_with(
        prompt_name="the return value",
        t=int,
        context=Context(description),
        default=NoDefault,
    )
    assert m.args.params == [("a", 1)]
    assert m.return_value == 0
