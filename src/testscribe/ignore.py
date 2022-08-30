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


class IgnoreReturnValue:
    def __repr__(self):
        # Use the string as the return value of a mock call.
        # It has to be a valid expression since it will be used in the generated test.
        return "'Ignored'"


# Use this variable when the special input expression "ignore" is used for a mock
# return value to ignore the return value.
# It's useful if the return value is not used in the production code.
IGNORED = IgnoreReturnValue()
