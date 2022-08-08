import test_data.person
import test_data.service
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.search_person import search_person_age


def test_search_person_age():
    """
    new
    """
    service: test_data.service.Service = create_autospec(spec=test_data.service.Service)
    service_search_person_return: test_data.person.Person = create_autospec(spec=test_data.person.Person)
    service.search_person.return_value = service_search_person_return
    service_search_person_return.age = 2
    result = search_person_age(service=service, name='a')
    assert result == 2
    service_mock_calls = get_normalized_mock_calls(service, test_data.service.Service)
    assert service_mock_calls == [
        call.search_person(name='a'),
    ]
    service_search_person_return.assert_not_called()
