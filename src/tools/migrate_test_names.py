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

import typer
from typer import Argument, Option

from testscribe.execution_util import init, get_all_scribe_files
from testscribe.load_scribe_file import load_scribe_file
from testscribe.model_type import TestModel
from testscribe.save_scribe_file import generate_scribe_file
from testscribe.util import remove_trailing_numbers

app = typer.Typer(name="migrate_test_names")
logger = logging.getLogger(__name__)


@app.command()
def file(
    scribe_file: Path = Argument(
        ...,
        help="The source file to migrate",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Generate short test names in the target files
    """
    migrate_file(scribe_file)


@app.command()
def all_files(
    output_root_dir: Optional[Path] = Option(
        None,
        help="The root directory of the output test files",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Generate short test names in the scribe files in the output directory

    """
    config = init()
    if not output_root_dir:
        output_root_dir = config.output_root_path
    total = 0
    for p in get_all_scribe_files(output_root_dir):
        migrate_file(p)
        total += 1
    print(f"Migrated {total} files.")
    return total


def migrate_file(scribe_file: Path):
    print(f"migrate {scribe_file}")
    all_tests = load_scribe_file(scribe_file)
    for t in all_tests.tests:
        migrate_one_test(t)
    generate_scribe_file(scribe_file_path=scribe_file, all_tests=all_tests)


def migrate_one_test(t: TestModel):
    name = t.name
    if t.short_name:
        return
    t.short_name = infer_short_name(name=name, target_func_name=t.target_func_name)


def infer_short_name(name: str, target_func_name: str) -> str:
    print(f"migrate test: {name}")
    name = remove_trailing_numbers(name)
    name = remove_prefix(name=name, prefix="test_")
    name = remove_function_name(name=name, func_name=target_func_name)
    print(f"short test name: {name}")
    return name


def remove_prefix(name: str, prefix: str) -> str:
    """
    :return:
    """
    if name.startswith(prefix):
        return name[len(prefix):]
    return name


def remove_function_name(name: str, func_name: str) -> str:
    if name == func_name:
        return "_"
    if name.startswith(func_name + "_"):
        return remove_prefix(name, func_name)
    return name


if __name__ == "__main__":
    app()
