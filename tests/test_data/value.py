from test_data.simple import C, foo, ReadOnlyData
import test_data.simple
from testscribe.transformer import transform_class, create_callable_model

callable_model_foo = create_callable_model(foo)

object_model_c = transform_class(C(a=1))
object_model_d = transform_class(ReadOnlyData(1))

simple_module = test_data.simple
