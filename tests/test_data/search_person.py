from test_data.service import Service


def search_person_age(service: Service, name: str) -> int:
    p = service.search_person(name)
    if p is None:
        return 0
    else:
        return p.age


def search_person_age_with_fixed_service(name: str) -> int:
    """
    Example of internally direct instantiation of a dependency.

    :param name:
    :return:
    """
    service = Service("pre")
    p = service.search_person(name)
    if p is None:
        return 0
    else:
        return p.age
