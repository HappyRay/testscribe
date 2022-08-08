from typing import List

from attr import dataclass


@dataclass
class Person:
    name: str = ""
    age: int = 10


# Don't make this class dataclass to test the behavior when
# a class doesn't implement __repr__
class Family:
    husband: Person = None
    wife: Person = None
    kids: List[Person] = []

    def __init__(self, husband, wife, kids):
        self.husband = husband
        self.wife = wife
        self.kids = kids


def get_name(p: Person) -> str:
    return p.name


def get_age(p: Person) -> int:
    return p.age


def total_age(person_list: List[Person]) -> int:
    total = 0
    for p in person_list:
        total += p.age
    return total
