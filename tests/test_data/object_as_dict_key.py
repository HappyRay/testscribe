from test_data.simple import ReadOnlyData


def get_dict_with_object_key():
    return {ReadOnlyData(1): 2}
