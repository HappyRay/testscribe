from __future__ import annotations

import json

from test_data.person import Person
from test_data.service import Service


def gen_name(service: Service, keyword: str, start_number: int):
    name = service.search_a_name("key: " + keyword)
    num = service.search_a_number(start_number)
    num2 = service.search_a_number(start_number + 1)
    d = {"name": name, "number": num + num2}
    json_str = json.dumps(d)
    return json_str


def get_fixed_person_service_name(service: Service) -> str:
    """
    Demonstrate a method call on a dependency with an object as a parameter.

    :param service:
    :return:
    """
    p = Person(name="Alice", age=1)
    return service.get_name_with_prefix(p)
