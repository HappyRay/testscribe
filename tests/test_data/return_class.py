from test_data.person import Person
from test_data.product import ProductOwner, Product


def create_person(name: str, age: int):
    return Person(name, age)


def create_fixed_product_owner():
    return ProductOwner(owner=Person("a", 30), product=Product("p", 1))
