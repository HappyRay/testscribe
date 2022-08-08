from typing import Callable

from test_data.value import object_model_c
from test_scribe.model_type import ObjectModel, MockNameModel, ExpressionModel, ModuleModel, \
    SetModel, ExceptionModel
from test_scribe.transformer import transform_value


def callable_model_repr(c: Callable) -> str:
    m = transform_value(c)
    return repr(m)


def get_object_model_hash() -> int:
    return hash(object_model_c)


def get_object_model_repr(o: ObjectModel) -> str:
    return repr(o)


def get_mockname_model_hash() -> int:
    return hash(MockNameModel("a"))


def get_mockname_model_repr() -> str:
    return repr(MockNameModel("a"))


def get_mockname_model_str() -> str:
    return str(MockNameModel("a"))


def get_expression_model_repr() -> str:
    return repr(ExpressionModel("a + 1"))


def get_expression_model_str() -> str:
    return str(ExpressionModel("a + 1"))


def get_module_model_str() -> str:
    return str(ModuleModel("a.b"))


def get_set_model_repr() -> str:
    return repr(SetModel([1, 2]))


def get_exception_model_str() -> str:
    return str(ExceptionModel(type="TypeError", message="wrong type"))
