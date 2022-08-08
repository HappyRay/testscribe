import test_data.simple
from fixture.helper import create_mock_proxy
from test_scribe.value_input_util import is_simple_value


def test_is_simple_value_mock():
    # This test can't be generated because MockProxy
    # is a special type and is replaced with a Mock object
    # when running the test.
    r = is_simple_value(create_mock_proxy(spec=test_data.simple.C))
    assert r is True
