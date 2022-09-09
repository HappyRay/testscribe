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

import logging.config
from pathlib import Path
from typing import Optional

import typer
from typer import Argument, Option

from testscribe import global_var
from testscribe.create_test_cmd import create_test
from testscribe.delete_test_cmd import delete_test
from testscribe.exception_decorator import exception_handler
from testscribe.move_cmd import move_tests
from testscribe.sync_cmd import regenerate_tests, regenerate_all_tests
from testscribe.update_test_cmd import update_test_cmd

app = typer.Typer(name="testscribe")
logger = logging.getLogger(__name__)

config_file_option = Option(
    None,
    help="The config file",
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=False,
)


@app.command()
@exception_handler
def create(
    source_file: Path = Argument(
        ...,
        help="The source file to test",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    function_name: str = Argument(..., help="The function to test"),
    output_root_dir: Optional[Path] = Option(
        None,
        help="The root directory of the output test files",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),  # useful for a quick test without creating or modifying a config file
    ask_for_test_name: bool = Option(True, help="Allow test names to be modified"),
    ask_for_description: bool = Option(True, help="Allow adding a test description"),
    config_file: Optional[Path] = config_file_option,
):
    """
    Generate a new test.

    :param config_file:
    :param ask_for_description:
    :param ask_for_test_name:
    :param source_file:
    :param function_name:
    :param output_root_dir:
    :return:
    """
    return create_test(
        source_file=source_file,
        function_name=function_name,
        output_root_dir=output_root_dir,
        ask_for_test_name=ask_for_test_name,
        ask_for_description=ask_for_description,
        config_file_path=config_file,
    )


@app.command()
@exception_handler
def delete(
    scribe_file_path: Path = Argument(
        ...,
        help="The testscribe file that contains the test to delete",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    test_name: str = Argument(..., help="The name of the test to delete"),
):
    """
    Delete a test. This will delete the test from both the testscribe file
    and the unit test file.

    :param scribe_file_path:
    :param test_name:
    :return:
    """
    return delete_test(scribe_file_path=scribe_file_path, test_name=test_name)


@app.command()
@exception_handler
def sync(
    scribe_file_path: Path = Argument(
        ...,
        help="The testscribe file to sync",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Regenerate the unit test file.

    :param scribe_file_path:
    :return:
    """
    return regenerate_tests(scribe_file_path=scribe_file_path)


@app.command()
@exception_handler
def sync_all(
        config_file: Optional[Path] = config_file_option,
):
    """
    Regenerate all unit test files under the configured test root.
    """
    return regenerate_all_tests(config_file)


@app.command()
@exception_handler
def update(
    scribe_file_path: Path = Argument(
        ...,
        help="The testscribe file to update",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    test_name: str = Argument("", help="The name of the test to update"),
) -> int:
    """
    Update the selected test.

    :param test_name:
    :param scribe_file_path:
    :return:
    """
    # The user defined setup function may call patch.
    # make sure the mode is set up before the setup function is called.
    global_var.g_test_generating_mode = True
    return update_test_cmd(scribe_file_path=scribe_file_path, test_name=test_name)


@app.command()
@exception_handler
def move(
    source_file: Path = Argument(
        ...,
        help="The source file that contains the symbol",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    class_or_function_name: str = Argument(
        ...,
        help="The name of the function or class that has moved."
        " To move tests for methods, use the class name of the methods.",
    ),
    config_file: Optional[Path] = config_file_option,
):
    """
    Move tests for a function to their new files corresponding to the new module
    to which the function has moved.
    """
    return move_tests(
        source_file=source_file,
        class_or_function_name=class_or_function_name,
        config_file_path=config_file,
    )


if __name__ == "__main__":  # pragma: no cover
    app()
