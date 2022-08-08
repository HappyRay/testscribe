import test_data.car
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.property_access2 import print_car_year_twice


def test_print_car_year_twice():
    m_car: test_data.car.Car = create_autospec(spec=test_data.car.Car)
    m_car.year = 1
    result = print_car_year_twice(c=m_car)
    assert result == '1, 1'
    m_car.assert_not_called()
