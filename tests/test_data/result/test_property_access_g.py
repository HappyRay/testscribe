import test_data.car
from testscribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_data.property_access import get_car_year


def test_get_car_year():
    m_car: test_data.car.Car = create_autospec(spec=test_data.car.Car)
    m_car.year = 1
    result = get_car_year(c=m_car)
    assert result == 1
    m_car.assert_not_called()
