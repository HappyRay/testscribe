from io import StringIO

from testscribe.load_scribe_file import load_from_yaml


def load_object_model(yaml_str: str):
    """
    Convert a string to a stream for input using code

    :param yaml_str:
    :return:
    """
    with StringIO(yaml_str) as stream:
        return load_from_yaml(stream=stream)
