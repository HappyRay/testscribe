import test_data.echo
import test_data.greet
import testscribe.execution
import testscribe.namedvalues
from wrapper.execution_wrapper import create_instance_wrapper, get_args_and_call_wrapper


def test_create_instance_wrapper():
    result = create_instance_wrapper()
    assert isinstance(result, testscribe.execution.CallResult)
    assert isinstance(result.arguments, testscribe.namedvalues.NamedValues)
    assert repr(result.arguments) == "NamedValues([('my_name', 'a')])"
    assert isinstance(result.result, test_data.greet.Greeter)
    assert result.result.my_name == 'a'
    assert result.exception is None


def test_get_args_and_call_wrapper_method():
    result = get_args_and_call_wrapper(func=test_data.greet.Greeter("a").greet)
    assert isinstance(result, testscribe.execution.CallResult)
    assert repr(result) == "CallResult(arguments=NamedValues([('to', 'b')]), result='Hello b. My name is a', exception=None)"


def test_get_args_and_call_wrapper_function():
    result = get_args_and_call_wrapper(func=test_data.echo.echo)
    assert isinstance(result, testscribe.execution.CallResult)
    assert repr(result) == "CallResult(arguments=NamedValues([('v', 'b')]), result='b', exception=None)"
