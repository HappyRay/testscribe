from pathlib import Path

from test_scribe.execution_util import get_all_scribe_files


def get_all_scribe_files_wrapper(root_path: Path):
    """
    Translate it into a list of relative paths for easier testing.
    """
    return [p.relative_to(root_path) for p in get_all_scribe_files(root_path)]
