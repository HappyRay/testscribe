from wrapper.tag_repr import representation_of_class_tag, representation_of_class_tag_list


def test_representation_of_class_tag():
    result = representation_of_class_tag()
    assert result == "Object(type (test_data.simple.C), members ({'a': 1}))"


def test_representation_of_class_tag_list():
    result = representation_of_class_tag_list()
    assert result == "[Object(type (test_data.simple.C), members ({'a': 1}))]"
