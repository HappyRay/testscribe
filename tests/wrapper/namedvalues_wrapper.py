from testscribe.namedvalues import NamedValues


def get_repr_of_named_values(nv: NamedValues) -> str:
    return repr(nv)


def get_item_via_index():
    return NamedValues([("a", 1), ("b", 2)])[1]
