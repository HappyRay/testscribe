from wrapper.cli_wrapper import run_cmd_help, run_cmd_without_args, run_create_cmd, run_create_cmd_with_file_name_only, run_help


def test_run_cmd_help_sync():
    result = run_cmd_help(cmd_name='sync')
    assert result == """\
Usage: test_scribe sync [OPTIONS] SCRIBE_FILE_PATH

  Regenerate the unit test file.

  :param scribe_file_path: :return:

Arguments:
  SCRIBE_FILE_PATH  The test_scribe file to sync  [required]

Options:
  --help  Show this message and exit.
"""


def test_run_cmd_help_delete():
    result = run_cmd_help(cmd_name='delete')
    assert result == """\
Usage: test_scribe delete [OPTIONS] SCRIBE_FILE_PATH [TEST_NAME]

  Delete a test. This will delete the test from both the test_scribe file and
  the unit test file.

  :param scribe_file_path: :param test_name: :return:

Arguments:
  SCRIBE_FILE_PATH  The test_scribe file to modify  [required]
  [TEST_NAME]       The name of the test to be removed

Options:
  --help  Show this message and exit.
"""


def test_run_cmd_help_update():
    result = run_cmd_help(cmd_name='update')
    assert result == """\
Usage: test_scribe update [OPTIONS] SCRIBE_FILE_PATH [TEST_NAME]

  Update the selected test.

  :param test_name: :param scribe_file_path: :return:

Arguments:
  SCRIBE_FILE_PATH  The test_scribe file to update  [required]
  [TEST_NAME]       The name of the test to update

Options:
  --help  Show this message and exit.
"""


def test_run_cmd_help_create():
    result = run_cmd_help(cmd_name='create')
    assert result == """\
Usage: test_scribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME

  Generate a new test.

  :param config_file: :param ask_for_description: :param ask_for_test_name:
  :param source_file: :param function_name: :param output_root_dir: :return:

Arguments:
  SOURCE_FILE    The source file to test  [required]
  FUNCTION_NAME  The function to test  [required]

Options:
  --output-root-dir DIRECTORY     The root directory of the output test files
  --ask-for-test-name / --no-ask-for-test-name
                                  Allow test names to be modified  [default:
                                  ask-for-test-name]
  --ask-for-description / --no-ask-for-description
                                  Allow adding a test description  [default:
                                  ask-for-description]
  --config-file FILE              The config file
  --help                          Show this message and exit.
"""


def test_run_cmd_help_move():
    result = run_cmd_help(cmd_name='move')
    assert result == """\
Usage: test_scribe move [OPTIONS] SOURCE_FILE CLASS_OR_FUNCTION_NAME

  Move tests for a function to their new files corresponding to the new module
  to which the function has moved.

Arguments:
  SOURCE_FILE             The source file that contains the symbol  [required]
  CLASS_OR_FUNCTION_NAME  The name of the function or class that has moved
                          [required]

Options:
  --output-root-dir DIRECTORY  The root directory of the output test files
  --help                       Show this message and exit.
"""


def test_cli_sync_cmd_with_missing_arguments_should_show_usage():
    result = run_cmd_without_args(cmd='sync')
    assert result == """\
Usage: test_scribe sync [OPTIONS] SCRIBE_FILE_PATH
Try 'test_scribe sync --help' for help.

Error: Missing argument 'SCRIBE_FILE_PATH'.
"""


def test_cli_update_cmd_with_missing_argument_should_show_usage():
    result = run_cmd_without_args(cmd='update')
    assert result == """\
Usage: test_scribe update [OPTIONS] SCRIBE_FILE_PATH [TEST_NAME]
Try 'test_scribe update --help' for help.

Error: Missing argument 'SCRIBE_FILE_PATH'.
"""


def test_cli_delete_cmd_missing_arguments_should_show_usage():
    result = run_cmd_without_args(cmd='delete')
    assert result == """\
Usage: test_scribe delete [OPTIONS] SCRIBE_FILE_PATH [TEST_NAME]
Try 'test_scribe delete --help' for help.

Error: Missing argument 'SCRIBE_FILE_PATH'.
"""


def test_cli_incorrect_file_argument_should_show_usage():
    result = run_create_cmd(additional_args=['do_not_exist'])
    assert result == """\
Usage: test_scribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME
Try 'test_scribe create --help' for help.

Error: Invalid value for 'SOURCE_FILE': File 'do_not_exist' does not exist.
"""


def test_cli_missing_file_name_should_show_usage():
    result = run_create_cmd(additional_args=[])
    assert result == """\
Usage: test_scribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME
Try 'test_scribe create --help' for help.

Error: Missing argument 'SOURCE_FILE'.
"""


def test_cli_create_cmd_without_function_name_should_show_usage():
    result = run_create_cmd_with_file_name_only()
    assert result == """\
Usage: test_scribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME
Try 'test_scribe create --help' for help.

Error: Missing argument 'FUNCTION_NAME'.
"""


def test_run_help():
    result = run_help()
    assert result == """\
Usage: test_scribe [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create    Generate a new test.
  delete    Delete a test.
  move      Move tests for a function to their new files corresponding to...
  sync      Regenerate the unit test file.
  sync-all  Regenerate all unit test files under the generated test root.
  update    Update the selected test.
"""
