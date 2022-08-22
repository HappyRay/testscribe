from io import StringIO
from typing import Any

from testscribe.save_scribe_file import save_to_yaml
from testscribe.transformer import transform_class


def save_object_model(v):
    object_model = transform_class(v)
    return save_obj_to_yaml(object_model)


def save_obj_to_yaml(obj: Any) -> str:
    with StringIO() as stream:
        save_to_yaml(data=obj, stream=stream)
        return stream.getvalue()
