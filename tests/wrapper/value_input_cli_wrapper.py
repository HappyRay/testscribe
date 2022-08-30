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

from unittest.mock import patch, create_autospec

from click import prompt
from click.exceptions import Abort

from testscribe.value_input_cli import get_one_value_cli


def get_one_value_cli_wrapper_abort():
    """
    Simulate users type ctrl-c to abort the program
    The patch interferes with the tool itself. Thus, it has to use a wrapper.
    """
    m_prompt = create_autospec(prompt, side_effect=Abort())
    with patch("testscribe.value_input_cli.prompt", m_prompt):
        get_one_value_cli(prompt_name="p", t=str, default="d")
