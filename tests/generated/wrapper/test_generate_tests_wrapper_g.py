from wrapper.generate_tests_wrapper import add_module_names_from_class_tag_complex_class


def test_add_module_names_from_class_tag_complex_class():
    result = add_module_names_from_class_tag_complex_class()
    assert result == ['test_data.product', 'test_data.person', 'test_data.product']
