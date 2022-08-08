import test_scribe.namedvalues
import test_scribe.special_type
from test_scribe.parameter_value_input import get_default_value_from_old_params


def test_get_default_value_from_old_params_no_name_match_index_out_of_bound():
    result = get_default_value_from_old_params(default=test_scribe.namedvalues.NamedValues([('a', 1), ('b', 2)]), index=2, name='c')
    assert result == test_scribe.special_type.NoDefault


def test_get_default_value_from_old_params_no_name_match_use_index():
    result = get_default_value_from_old_params(default=test_scribe.namedvalues.NamedValues([('a',1), ('b',2)]), index=1, name='c')
    assert result == 2
