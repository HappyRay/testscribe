from test_data.calculator import add


def test_add_1():
    result = add(a=3, b=4)
    assert result == 7


def test_add():
    result = add(a=1, b=2)
    assert result == 3
