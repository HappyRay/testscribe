import test_data.person
import test_data.product
from test_data.return_class import create_fixed_product_owner


def test_create_fixed_product_owner():
    result = create_fixed_product_owner()
    assert isinstance(result, test_data.product.ProductOwner)
    assert isinstance(result.owner, test_data.person.Person)
    assert repr(result.owner) == "Person(name='a', age=30)"
    assert isinstance(result.product, test_data.product.Product)
    assert repr(result.product) == "Product(name='p', price=1)"
