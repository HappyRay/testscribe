import test_data.person
from test_data.return_list_of_objects import create_person_list


def test_create_person_list():
    result = create_person_list()
    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], test_data.person.Person)
    assert repr(result[0]) == "Person(name='a', age=1)"
    assert isinstance(result[1], test_data.person.Person)
    assert repr(result[1]) == "Person(name='b', age=2)"
