from test_data.person import Person


class Service:
    """
    Simulate an external complex service maybe over network.
    """

    def __init__(self, prefix: str):
        self.prefix = prefix

    def search_a_name(self, keyword: str) -> str:
        return f"{keyword}: {self.prefix} Alice"

    def search_a_number(self, seed_number: int) -> int:
        return seed_number + 1

    def search_person(self, name: str) -> Person:
        return Person(name="a", age=1)

    def get_name_with_prefix(self, p: Person) -> str:
        return self.prefix + p.name
