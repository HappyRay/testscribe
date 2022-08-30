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

# Reflection related functions that don't depend on other modules in this project
from typing import Any

from testscribe.type_util import is_a_class_instance


def get_full_module_name(symbol: Any) -> str:
    if hasattr(symbol, "__module__"):
        return symbol.__module__
    else:
        return ""


def get_class_instance_repr_with_full_name(instance) -> str:
    assert is_a_class_instance(instance)
    full_module_name = get_full_module_name(instance)
    module_str = full_module_name + "." if full_module_name else ""
    return f"{module_str}{repr(instance)}"
