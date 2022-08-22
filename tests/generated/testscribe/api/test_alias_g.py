from unittest.mock import patch
from testscribe.api.alias import define_alias


def test_define_alias():
    with patch('testscribe.api.alias.g_aliases', {'A': '2'}):
        result = define_alias(alias='foo', full_str='bar')
    assert result == {'A': '2', 'foo': 'bar'}
