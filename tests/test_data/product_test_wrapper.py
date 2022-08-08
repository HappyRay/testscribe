from test_data.product import Product, get_a_product_total, ProductFactory


def get_a_product_total_using_mocks(p1: Product, p2: Product, factory: ProductFactory):
    return get_a_product_total(factory)
