from fixture.helper import patch_globals_modified_by_mock_proxy
from test_data.simple import ReadOnlyData, SimpleDataClass
from testscribe.mock_proxy import MockProxy
from testscribe.model_type import MockNameModel


def get_dict(d: ReadOnlyData):
    return {d: 1}


def use_not_hashable():
    patch_globals_modified_by_mock_proxy()
    return hash(MockProxy(spec=SimpleDataClass, name="s"))


def hash_mock_proxy():
    patch_globals_modified_by_mock_proxy()
    name = "d"
    proxy_hash = hash(MockProxy(spec=ReadOnlyData, name=name))
    mock_name_hash = hash(MockNameModel(name))
    assert proxy_hash == mock_name_hash
    return proxy_hash
