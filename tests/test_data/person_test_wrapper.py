from test_data.person import Person, total_age


def get_total_age_of_people_real_objects():
    p1 = Person("a", 1)
    p2 = Person("b", 2)
    return total_age([p1, p2])


def get_total_age_of_two_people_using_mocks(p1: Person, p2: Person):
    return total_age([p1, p2])
