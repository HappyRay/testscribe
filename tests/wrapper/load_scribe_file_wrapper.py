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

from io import StringIO

from testscribe.load_scribe_file import load_from_yaml


def load_object_model(yaml_str: str):
    """
    Convert a string to a stream for input using code

    :param yaml_str:
    :return:
    """
    with StringIO(yaml_str) as stream:
        return load_from_yaml(stream=stream)
