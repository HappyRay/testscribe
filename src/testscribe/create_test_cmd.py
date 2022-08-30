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

import logging
from pathlib import Path
from typing import Optional

from testscribe import global_var
from testscribe.config import Config
from testscribe.execution import execute_and_generate, run_setup_func
from testscribe.execution_util import init
from testscribe.file_info import get_module
from testscribe.input_params import create_input_params, get_scribe_file_path
from testscribe.load_scribe_file import load_or_create_model
from testscribe.log import log

logger = logging.getLogger(__name__)


def get_output_root_dir(output_root_dir: Optional[Path], config: Config) -> Path:
    if output_root_dir:
        log(f"Output root directory cmd line option: {output_root_dir}")
    else:
        # use the one in the config
        output_root_dir = config.output_root_path
    normalized_output_root_dir = output_root_dir.resolve()
    log(f"Output root directory: {normalized_output_root_dir}")
    return normalized_output_root_dir


def create_test(
    source_file: Path,
    function_name: str,
    output_root_dir: Optional[Path],
    ask_for_test_name: bool,
    ask_for_description: bool,
    config_file_path: Optional[Path],
):
    # The user defined setup function may call patch.
    # make sure the mode is set up before the setup function is called.
    global_var.g_test_generating_mode = True
    config = init(config_file_path=config_file_path)

    log(f"Source file to test: {source_file}")
    log(f"Function to test: {function_name}")
    module = get_module(source_file)
    log(f"Target module to test: {module.get_module_str()}")

    normalized_output_root_dir = get_output_root_dir(output_root_dir, config)
    input_params = create_input_params(
        module=module,
        function_name=function_name,
        output_root_dir=normalized_output_root_dir,
        ask_for_test_name=ask_for_test_name,
        ask_for_description=ask_for_description,
    )
    scribe_file_path = get_scribe_file_path(
        output_root_dir=normalized_output_root_dir, module=module
    )
    all_tests = load_or_create_model(
        file_path=scribe_file_path,
        full_module_name=input_params.module.get_module_str(),
    )
    run_setup_func(config.setup_function)
    execute_and_generate(
        input_params=input_params, all_tests=all_tests, index_of_test_to_update=-1
    )
