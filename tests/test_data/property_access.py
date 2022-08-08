from test_data.car import Car


def get_car_name(c: Car) -> str:
    """
    Because the name property is not annotated with type information,
    the value has to be quoted.
    :param c:
    :return:
    """
    return c.name


def get_car_year(c: Car) -> int:
    """
    Because the year property is annotated with type information,
    the value can be entered more easily.
    :param c:
    :return:
    """
    return c.year
