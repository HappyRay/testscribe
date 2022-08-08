from typing import List

from typer.testing import CliRunner

from test_scribe.main import app


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
