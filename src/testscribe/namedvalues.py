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
from typing import Tuple, Any, Iterable

from testscribe.value_util import get_value_repr

logger = logging.getLogger(__name__)


class NameNotFound:
    """
    Marker object for not having the name in the NamedValues instance.
    Note that None can be a valid value.
    """


class NamedValues:
    def __init__(self, name_value_list: Iterable[Tuple[str, Any]] = []):
        self.params = list(name_value_list)

    def __getitem__(self, index: int) -> Tuple[str, Any]:
        """
        Support getting an item via its index
        e.g. see testscribe.value_input.get_default_value_from_old_params
        """
        return self.params[index]

    def get_size(self):
        return len(self.params)

    def get_value_by_name(self, name: str):
        for n, value in self.params:
            if n == name:
                return value
        return NameNotFound

    def __repr__(self):
        return f"NamedValues({repr(self.params)})"

    def as_arg_str(self):
        # Some functions e.g. some builtin functions may not have the parameter
        # names available.
        arg_list = [format_one_param(name=k, value=v) for k, v in self.params]
        arg_str = ", ".join(arg_list)
        return arg_str

    def as_list(self):
        return list(self.params)


def format_one_param(name: str, value: Any) -> str:
    value_repr = get_value_repr(value)
    if name:
        return f"{name}={value_repr}"
    else:
        return value_repr
