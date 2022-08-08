import sys
from pathlib import Path

from conftest import assert_same
from fixture.helper import get_project_root_path
from test_scribe.config import init_config, add_additional_python_paths


def convert_to_absolute_path_str(s: str) -> str:
    return str(Path(s).absolute())


def init_config_wrapper():
    # make a copy
    old_sys_path = list(sys.path)
    config = init_config(
        config_file_path=get_project_root_path() / "test-scribe-config.yml"
    )
    # The sys.path may contain absolute paths and paths that depend on
    # the environment in which it runs. So it doesn't work to return
    # the new sys.path to have the assertions generated.
    assert_same(actual=sys.path, expected=old_sys_path + ["python/src", "python/tests"])
    return config


def add_additional_python_paths_no_key() -> None:
    old_sys_path = list(sys.path)
    add_additional_python_paths({})
    assert_same(actual=sys.path, expected=old_sys_path)
