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

from typing import List

from typer.testing import CliRunner

from testscribe.__main__ import app


def run(args: List[str]):
    runner = CliRunner()
    print(f"args: {args}")
    result = runner.invoke(app, args)
    return result.stdout


def run_create_cmd(additional_args: List[str]):
    args = ["create"] + additional_args
    return run(args)


def run_create_cmd_with_file_name_only():
    current_file_path = __file__
    return run_create_cmd([current_file_path])


def run_cmd_without_args(cmd: str):
    args = [cmd]
    return run(args)


def run_help():
    return run("--help")


def run_cmd_help(cmd_name: str):
    return run([cmd_name] + ["--help"])
