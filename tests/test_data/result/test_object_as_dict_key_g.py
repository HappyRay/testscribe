import test_data.simple
from test_data.object_as_dict_key import get_dict_with_object_key


def test_get_dict_with_object_key():
    result = get_dict_with_object_key()
    assert result == {test_data.simple.ReadOnlyData(a=1): 2}
