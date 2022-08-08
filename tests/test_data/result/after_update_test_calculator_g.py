from test_data.calculator import add


def test_add():
    """
    new
    """
    result = add(a=1, b=2)
    assert result == 3
