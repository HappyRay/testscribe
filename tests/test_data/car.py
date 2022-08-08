class Car:
    year: int

    def __init__(self, year: int, name: str):
        self.year = year
        self.name = name

    def get_year(self) -> int:
        return self.year

    def get_name(self) -> str:
        return self.name
