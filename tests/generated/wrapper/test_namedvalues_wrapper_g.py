import testscribe.namedvalues
from wrapper.namedvalues_wrapper import get_item_via_index, get_repr_of_named_values


def test_get_item_via_index():
    result = get_item_via_index()
    assert result == ('b', 2)


def test_get_repr_of_named_values_default_constructor():
    result = get_repr_of_named_values(nv=testscribe.namedvalues.NamedValues())
    assert result == 'NamedValues([])'


def test_get_repr_of_named_values():
    result = get_repr_of_named_values(nv=testscribe.namedvalues.NamedValues([('a', 1)]))
    assert result == "NamedValues([('a', 1)])"
