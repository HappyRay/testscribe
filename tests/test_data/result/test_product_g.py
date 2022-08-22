import test_data.product
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.product import get_a_product_total


def test_get_a_product_total():
    m_product_factory: test_data.product.ProductFactory = create_autospec(spec=test_data.product.ProductFactory)
    m_product: test_data.product.Product = create_autospec(spec=test_data.product.Product)
    m_product_1: test_data.product.Product = create_autospec(spec=test_data.product.Product)
    m_product_factory.create_sample_products.return_value = [m_product, m_product_1]
    m_product.price = 1
    m_product_1.price = 2
    result = get_a_product_total(factory=m_product_factory)
    assert result == 3
    m_product_factory_mock_calls = get_normalized_mock_calls(m_product_factory, test_data.product.ProductFactory)
    assert m_product_factory_mock_calls == [
        call.create_sample_products(prefix='a', num=2),
    ]
    m_product.assert_not_called()
    m_product_1.assert_not_called()
