import test_data.person
from test_data.return_class import create_person


def test_create_person():
    result = create_person(name='a', age=1)
    assert isinstance(result, test_data.person.Person)
    assert repr(result) == "Person(name='a', age=1)"
