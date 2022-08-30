#  Copyright 2022 Ruiguo (Ray) Yang
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

from __future__ import annotations

import logging
from typing import List, Any

from testscribe import global_var
from testscribe.custom_type import Spec
from testscribe.log import log
from testscribe.mock_call import MockCall
from testscribe.mock_proxy_support import (
    create_mock_name,
    check_unsupported_attributes,
    create_mock_call,
    get_mock_attribute_value,
)
from testscribe.reflection_util import is_method
from testscribe.util import consistent_hash_str
from testscribe.value_util import get_value

logger = logging.getLogger(__name__)


class MockProxy:
    def __init__(self, spec: Spec, name: str = ""):
        # The internal attributes have _test_scribe_ postfix to reduce the chance
        # of collision with attributes of the targets being mocked.
        self.spec_test_scribe_ = spec  # the class or function it is mocking
        self.calls_test_scribe_: List[MockCall] = []
        mock_name = create_mock_name(name=name, spec=spec)
        self.name_test_scribe_ = mock_name
        self.attributes_test_scribe_ = {}
        self.attributes_transformed_test_scribe_ = {}

        global_var.g_name_mock_dict[mock_name] = self
        log(f"Created a mock: {get_proxy_str(self)}")

    def __getattr__(self, name):
        """
        Use __getattribute__ will result in a recursive call into
        __getattribute__ when method_calls attribute is used.
        see
        https://stackoverflow.com/questions/4295678/understanding-the-difference-between-getattr-and-getattribute

        :param name:
        :return:
        """
        logger.debug(f"__getattr__ called with {name}")
        # print_stack()

        check_unsupported_attributes(name)

        if name in self.attributes_test_scribe_:
            # Mocked property value can't change
            v = self.attributes_test_scribe_[name]
            logger.debug(f"Return existing attribute value({v})")
            return v

        if is_method(self.spec_test_scribe_, name):
            return record_mock_call(proxy=self, method_name=name)
        else:
            return record_attribute(proxy=self, attribute_name=name)

    def __call__(self, *args, **kwargs):
        # assume this is a constructor call or a function call
        # todo: support __call__
        mock_call = record_mock_call(proxy=self, method_name="")
        return mock_call.call_internal(*args, **kwargs)

    def __str__(self):
        # __getattr__ is not called with __str__
        call = self.__getattr__("__str__")
        return call.call_internal()

    def __enter__(self):
        # __getattr__ is not called with __enter__ nor __exit__
        # todo: fix the call stack display
        # log(f"__enter__ is called on {self}")
        call = self.__getattr__("__enter__")
        return call.call_internal()

    def __exit__(self, exc_type, exc_value, traceback):
        # log(f"__exit__ is called on {self}.")
        call = self.__getattr__("__exit__")
        return call.call_internal(exc_type, exc_value, traceback)

    def __hash__(self):
        if is_method(self.spec_test_scribe_, "__hash__"):
            # This simple approach doesn't allow the flexibility of mocking __hash__
            # differently. Note that the mock object is transformed into MockName
            # and the __hash__ method may be called when generating the code
            # Let's favor simplity for now.

            # return the hash of self is problematic since the mock object is stored
            # and transformed as MockName. The hash function needs to return
            # consistent results.
            return consistent_hash_str(self.name_test_scribe_)
        else:
            raise TypeError(
                f"The mock target {self.spec_test_scribe_} is not hashable."
            )

    @property
    def __class__(self):
        """
        Override this method to allow the mock object to pass the isinstance check
        if the spec is a class/type.

        Modeled after NonCallableMock.__class__
        @property is important to allow overriding this property.
        :return:
        """
        spec = self.spec_test_scribe_
        if isinstance(spec, type):
            return spec
        else:
            return type(spec)


def get_proxy_str(m: MockProxy):
    return f"Mock: name ({m.name_test_scribe_}) spec ({m.spec_test_scribe_})"


def record_mock_call(proxy: MockProxy, method_name: str) -> MockCall:
    calls = proxy.calls_test_scribe_
    mock_call = create_mock_call(
        method_name=method_name,
        mock_name=proxy.name_test_scribe_,
        spec=proxy.spec_test_scribe_,
        mock_calls=calls,
    )
    calls.append(mock_call)
    return mock_call


def record_attribute(proxy: MockProxy, attribute_name: str) -> Any:
    input_value = get_mock_attribute_value(
        attribute_name=attribute_name,
        mock_name=proxy.name_test_scribe_,
        spec=proxy.spec_test_scribe_,
    )
    # avoid circular reference
    from testscribe.transformer import transform_value

    # keep a copy of the transformed original value
    # in case the value is changed after execution.
    proxy.attributes_transformed_test_scribe_[attribute_name] = transform_value(
        input_value
    )

    value = get_value(input_value)
    proxy.attributes_test_scribe_[attribute_name] = value
    log(f"Mock attribute value: {repr(value)}")

    return value


def is_mock_proxy(obj) -> bool:
    # can't use isinstance on Mock objects because they override __class__
    return issubclass(type(obj), MockProxy)
