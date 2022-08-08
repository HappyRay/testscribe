from typer.testing import CliRunner

from fixture.helper import remove_project_root_directory_prefix
from test_data.dummy_app import app


def run_dummy_app():
    runner = CliRunner()
    result = runner.invoke(app)
    out = result.stdout
    print(f"output:\n{out}")
    out_with_absolute_directory_removed = remove_project_root_directory_prefix(out)
    return result.exit_code, out_with_absolute_directory_removed
