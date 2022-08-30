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
from pathlib import Path

from yaml import dump, add_representer

from testscribe.execution_util import remove_file_if_no_test
from testscribe.log import log
from testscribe.model_encoder import encode_model
from testscribe.model_type import AllTests
from testscribe.yaml_tag import add_representer_for_custom_tags

logger = logging.getLogger(__name__)


def generate_scribe_file(scribe_file_path: Path, all_tests: AllTests) -> None:
    if remove_file_if_no_test(file_path=scribe_file_path, tests=all_tests.tests):
        return
    content = encode_model(all_tests)
    # todo: validate the content first before writing to the file
    with scribe_file_path.open(mode="w") as f:
        save_to_yaml(data=content, stream=f)
    log(f"Wrote the generated scribe file to: {scribe_file_path}")


def save_to_yaml(data, stream):
    configure_yaml()
    # Before pyyaml 5.1 the directory keys are sorted. Since 5.1 it is still the default,
    # but the sort_keys parameter was added.
    # It is desirable to control the order so that it is easier to read.
    dump(data=data, stream=stream, sort_keys=False)


def configure_yaml():
    add_representer(str, string_presenter)
    add_representer_for_custom_tags()


def string_presenter(dumper, data):
    """
    Control how the strings are formatted.
    see
    https://yaml-multiline.info/
    https://www.generacodice.com/en/articolo/3292961/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data

    :param dumper:
    :param data:
    :return:
    """
    length = len(data.splitlines())
    if length > 1:
        # only use the block style for multi line strings
        # The flow style is simpler and easier to read for a single line string.
        style = "|"
    else:
        style = None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style)
