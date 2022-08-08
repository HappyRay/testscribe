from unittest.mock import patch
from test_data.patch_in_method import MethodPatched


def test_foo():
    with patch('test_data.simple.INT_VALUE', 2):
        instance = MethodPatched(i=1)
        result = instance.foo()
    assert result == 3
