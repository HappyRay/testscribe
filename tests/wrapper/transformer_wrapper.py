from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data import simple
from test_data.simple import C
from testscribe.mock_proxy import MockProxy
from testscribe.transformer import transform_value


def tranform_module():
    """
    The tool can't automatically import the module using an expression
    like test_data.simple yet.

    :return:
    """
    return transform_value(simple)


def transform_mock_proxy():
    """
    Without the wrapper, the tool will generate a statement like
    result = transform_value(v=a)
    since the mockproxy object will be replaced by its name.
    It doesn't work in this special case.

    :return:
    """
    patch_globals_modified_by_mock_proxy()
    return transform_value(MockProxy(C, "a"))
