from wrapper.value_input_util_wrapper import transform_real_default_value_wrapper


def test_transform_real_default_value_wrapper():
    result = transform_real_default_value_wrapper()
    assert result == "m(spec, 'a')"
