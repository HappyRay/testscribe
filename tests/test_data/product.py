from dataclasses import dataclass
from typing import List

from test_data.person import Person


@dataclass
class Product:
    name: str
    price: int


class ProductFactory:
    def create_sample_products(self, prefix: str, num: int) -> List[Product]:
        return [Product(f"{prefix}.{n}", n * 10) for n in range(num)]


def get_a_product_total(factory: ProductFactory):
    products = factory.create_sample_products("a", 2)
    total = 0
    for p in products:
        total += p.price
    return total


# Don't make this class dataclass to test the behavior when
# a class doesn't implement __repr__
class ProductOwner:
    owner: Person = None
    product: Product = None

    def __init__(self, owner, product):
        self.owner = owner
        self.product = product
