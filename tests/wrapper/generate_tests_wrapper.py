from test_data.person import Person
from test_data.product import ProductOwner, Product
from testscribe.gather_referenced_modules import get_module_names_from_value
from testscribe.transformer import transform_value


def add_module_names_from_class_tag_complex_class():
    """
    This wrapper makes it easier to construct the input with code.
    """
    v = transform_value(ProductOwner(owner=Person("a", 30), product=Product("p", 1)))
    return get_module_names_from_value(v)
