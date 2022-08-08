from wrapper.mock_api_wrapper import get_normalized_mock_calls_wrapper


def test_get_normalized_mock_calls_wrapper():
    result = get_normalized_mock_calls_wrapper()
    assert result == [('search_a_name', (), {'keyword': 'a'}), ('search_person', (), {'name': 'b'})]
