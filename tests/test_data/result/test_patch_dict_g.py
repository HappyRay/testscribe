from unittest.mock import patch
from test_data.patch_dict import get_patched_dict


def test_get_patched_dict():
    with patch('test_data.patch_dict.a_dict', {'b': 2}):
        result = get_patched_dict()
    assert result == {'b': 2}
