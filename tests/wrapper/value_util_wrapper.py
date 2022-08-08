from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data.simple import C
from test_scribe.mock_proxy import MockProxy
from test_scribe.value_util import get_value_repr


def get_value_repr_wrapper_mock_proxy():
    """
    Need this wrapper to avoid MockProxy to be translated to its name
    or a MagicMock object in the generated code.
    """
    patch_globals_modified_by_mock_proxy()
    return get_value_repr(MockProxy(spec=C, name="a"))
