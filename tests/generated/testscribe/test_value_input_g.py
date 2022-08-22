import testscribe.context
from testscribe.value_input import get_one_value


def test_get_one_value_none_type_1():
    result = get_one_value(prompt_name='p', t=type(None), context=testscribe.context.Context("foo"), default=None, name='n')
    assert result is None


def test_get_one_value_none_type():
    result = get_one_value(prompt_name='p', t=None, context=testscribe.context.Context("foo"), default=None, name='n')
    assert result is None
