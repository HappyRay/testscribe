from unittest.mock import patch
from test_scribe.api.alias import define_alias


def test_define_alias():
    with patch('test_scribe.api.alias.g_aliases', {'A': '2'}):
        result = define_alias(alias='foo', full_str='bar')
    assert result == {'A': '2', 'foo': 'bar'}
