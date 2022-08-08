from test_data.service import Service


def test_search_a_name():
    instance = Service(prefix='a')
    result = instance.search_a_name(keyword='b')
    assert result == 'b: a Alice'
