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

from dataclasses import dataclass

from testscribe.base_reflection_util import get_class_instance_repr_with_full_name


@dataclass
class UserTriggeredException:
    """
    Used in an input expression to cause a mock call to throw the
    given exception.
    """

    exception: BaseException

    def __repr__(self):
        """
        Custom repr to allow easier code generation
        :return:
        """
        return get_class_instance_repr_with_full_name(self.exception)
