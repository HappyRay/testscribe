from testscribe.mock_proxy import is_mock_proxy


def test_is_mock_proxy_false():
    result = is_mock_proxy(obj=1)
    assert result is False
