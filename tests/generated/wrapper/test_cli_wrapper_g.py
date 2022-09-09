from wrapper.cli_wrapper import run_cmd_help, run_cmd_without_args, run_create_cmd, run_create_cmd_with_file_name_only, run_help


def test_run_cmd_help_sync():
    result = run_cmd_help(cmd_name='sync')
    assert result == """\
                                                                                
 Usage: testscribe sync [OPTIONS] SCRIBE_FILE_PATH                              
                                                                                
 Regenerate the unit test file.                                                 
 :param scribe_file_path: :return:                                              
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    scribe_file_path      FILE  The testscribe file to sync [default: None] │
│                                  [required]                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

"""


def test_run_cmd_help_delete():
    result = run_cmd_help(cmd_name='delete')
    assert result == """\
                                                                                
 Usage: testscribe delete [OPTIONS] SCRIBE_FILE_PATH TEST_NAME                  
                                                                                
 Delete a test. This will delete the test from both the testscribe file and the 
 unit test file.                                                                
 :param scribe_file_path: :param test_name: :return:                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    scribe_file_path      FILE  The testscribe file that contains the test  │
│                                  to delete                                   │
│                                  [default: None]                             │
│                                  [required]                                  │
│ *    test_name             TEXT  The name of the test to delete              │
│                                  [default: None]                             │
│                                  [required]                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

"""


def test_run_cmd_help_update():
    result = run_cmd_help(cmd_name='update')
    assert result == """\
                                                                                
 Usage: testscribe update [OPTIONS] SCRIBE_FILE_PATH [TEST_NAME]                
                                                                                
 Update the selected test.                                                      
 :param test_name: :param scribe_file_path: :return:                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    scribe_file_path      FILE         The testscribe file to update        │
│                                         [default: None]                      │
│                                         [required]                           │
│      test_name             [TEST_NAME]  The name of the test to update       │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

"""


def test_run_cmd_help_create():
    result = run_cmd_help(cmd_name='create')
    assert result == """\
                                                                                
 Usage: testscribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME                   
                                                                                
 Generate a new test.                                                           
 :param config_file: :param ask_for_description: :param ask_for_test_name:      
 :param source_file: :param function_name: :param output_root_dir: :return:     
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    source_file        FILE  The source file to test [default: None]        │
│                               [required]                                     │
│ *    function_name      TEXT  The function to test [default: None]           │
│                               [required]                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output-root-dir                            DIRECTORY  The root directory   │
│                                                         of the output test   │
│                                                         files                │
│                                                         [default: None]      │
│ --ask-for-test-name    --no-ask-for-test…               Allow test names to  │
│                                                         be modified          │
│                                                         [default:            │
│                                                         ask-for-test-name]   │
│ --ask-for-descript…    --no-ask-for-desc…               Allow adding a test  │
│                                                         description          │
│                                                         [default:            │
│                                                         ask-for-description] │
│ --config-file                                FILE       The config file      │
│                                                         [default: None]      │
│ --help                                                  Show this message    │
│                                                         and exit.            │
╰──────────────────────────────────────────────────────────────────────────────╯

"""


def test_run_cmd_help_move():
    result = run_cmd_help(cmd_name='move')
    assert result == """\
                                                                                
 Usage: testscribe move [OPTIONS] SOURCE_FILE CLASS_OR_FUNCTION_NAME            
                                                                                
 Move tests for a function to their new files corresponding to the new module   
 to which the function has moved.                                               
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    source_file                 FILE  The source file that contains the     │
│                                        symbol                                │
│                                        [default: None]                       │
│                                        [required]                            │
│ *    class_or_function_name      TEXT  The name of the function or class     │
│                                        that has moved                        │
│                                        [default: None]                       │
│                                        [required]                            │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --output-root-dir        DIRECTORY  The root directory of the output test    │
│                                     files                                    │
│                                     [default: None]                          │
│ --help                              Show this message and exit.              │
╰──────────────────────────────────────────────────────────────────────────────╯

"""


def test_cli_sync_cmd_with_missing_arguments_should_show_usage():
    result = run_cmd_without_args(cmd='sync')
    assert result == """\
Usage: testscribe sync [OPTIONS] SCRIBE_FILE_PATH
Try 'testscribe sync --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'SCRIBE_FILE_PATH'.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
"""


def test_cli_update_cmd_with_missing_argument_should_show_usage():
    result = run_cmd_without_args(cmd='update')
    assert result == """\
Usage: testscribe update [OPTIONS] SCRIBE_FILE_PATH [TEST_NAME]
Try 'testscribe update --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'SCRIBE_FILE_PATH'.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
"""


def test_cli_delete_cmd_missing_arguments_should_show_usage():
    result = run_cmd_without_args(cmd='delete')
    assert result == """\
Usage: testscribe delete [OPTIONS] SCRIBE_FILE_PATH TEST_NAME
Try 'testscribe delete --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'SCRIBE_FILE_PATH'.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
"""


def test_cli_incorrect_file_argument_should_show_usage():
    result = run_create_cmd(additional_args=['do_not_exist'])
    assert result == """\
Usage: testscribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME
Try 'testscribe create --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Invalid value for 'SOURCE_FILE': File 'do_not_exist' does not exist.         │
╰──────────────────────────────────────────────────────────────────────────────╯
"""


def test_cli_missing_file_name_should_show_usage():
    result = run_create_cmd(additional_args=[])
    assert result == """\
Usage: testscribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME
Try 'testscribe create --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'SOURCE_FILE'.                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
"""


def test_cli_create_cmd_without_function_name_should_show_usage():
    result = run_create_cmd_with_file_name_only()
    assert result == """\
Usage: testscribe create [OPTIONS] SOURCE_FILE FUNCTION_NAME
Try 'testscribe create --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ Missing argument 'FUNCTION_NAME'.                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
"""


def test_run_help():
    result = run_help()
    assert result == """\
                                                                                
 Usage: testscribe [OPTIONS] COMMAND [ARGS]...                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershe  Install completion for  │
│                             ll|pwsh]                 the specified shell.    │
│                                                      [default: None]         │
│ --show-completion           [bash|zsh|fish|powershe  Show completion for the │
│                             ll|pwsh]                 specified shell, to     │
│                                                      copy it or customize    │
│                                                      the installation.       │
│                                                      [default: None]         │
│ --help                                               Show this message and   │
│                                                      exit.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create    Generate a new test.                                               │
│ delete    Delete a test. This will delete the test from both the testscribe  │
│           file and the unit test file.                                       │
│ move      Move tests for a function to their new files corresponding to the  │
│           new module to which the function has moved.                        │
│ sync      Regenerate the unit test file.                                     │
│ sync-all  Regenerate all unit test files under the generated test root.      │
│ update    Update the selected test.                                          │
╰──────────────────────────────────────────────────────────────────────────────╯

"""
