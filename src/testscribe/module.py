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

from typing import Collection, List


class Module:
    def __init__(self, module_names: Collection[str]):
        """

        :param module_names:a list of string representing the full module name.
        Parent module name comes first.
        """
        self.names = tuple(module_names)

    def get_package_name_list(self) -> List[str]:
        return list(self.names[:-1])

    def get_module_name_only(self) -> str:
        return self.names[-1]

    def get_module_str(self):
        return ".".join(self.names)


def get_module_from_str(name: str) -> Module:
    return Module(name.split("."))
