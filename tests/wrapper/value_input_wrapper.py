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

from testscribe.value_input_cli import post_process_raw_input
from testscribe.value_util import InputValue


def post_process_raw_input_wrapper_special_value():
    r = post_process_raw_input(raw_input_str="ignore", t=int)
    # InputValue has special handing. So translate it to a regular tuple here.
    assert isinstance(r, InputValue)
    return r.expression, r.value
