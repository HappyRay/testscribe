---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: my-home
title: home
---
# TestScribe: Unit test made easy

A tool to make python unit testing easier by automating the boring and repetitive parts.

# The idea
Unit tests should be as intuitive as testing a web page. 
Developers should be able to test a function by providing inputs interactively and 
verify outputs visually without having to write boilerplate code in most cases. 
The process is similar to a debugging session which answers
"what happens when I pass this input". 
Note that 
* mock objects' attributes and mock methods' return values are inputs
* parameter values to mock method calls are outputs

Additionally, the test runs are recorded both as traditional unit tests 
and a structured machine-readable format by the tool automatically. 
The machine-readable format will enable additional functionalities such as maintaining 
regression tests.

# Quick start
Follow the following steps to quickly try out the tool. 

It doesn't modify your existing files.
You can easily restore your original state, especially when you are using a version control system.

1. Add [testscribe](https://pypi.org/project/testscribe/) to your development python library dependencies.
    ```commandline
    pip install testscribe
    ```
2. In your activated python environment, run 
    ```commandline
    testscribe create "the path to your python file under test" "the name of the function under test"
    ```

3. Follow the prompts to provide inputs and inspect the outputs

4. [Optional] Use the generated test files for debugging, regression tests, etc.
The file locations can be found in the output.

# Command line help
Use the --help option to display help information from a command line.

    testscribe --help

output:

    Usage: testscribe [OPTIONS] COMMAND [ARGS]...

Use the --help option after a command name to display help information
for that command.

For example:

    testscribe create --help

# Required setup
Use your favorite tool to add [testscribe](https://pypi.org/project/testscribe/) to your development python 
library dependencies. Note that it is not needed as a production dependency.

# Optional setup
To take full advantage of the tool, some optional setups are needed.

## Quick launch for the Intellij/Pycharm IDE
Intellij and Pycharm IDEs support external tools and keyboard shortcuts.
You can leverage this support to launch the tool more easily and quickly.

### An example intellij external tool configuration for the create command 
Program: $ModuleSdkPath$

Arguments: -m testscribe create $FilePath$ $SelectedText$

To test a function, open the target file, highlight the function to test, invoke the configured external tool.
It's helpful to configure a keyboard shortcut to launch the external tool.

Other commands can be configured in a similar way.

### References
[Intellij external tools instructions](https://www.jetbrains.com/help/idea/settings-tools-external-tools.html)

[Intellij configure keyboard shortcut](https://www.jetbrains.com/help/idea/configuring-keyboard-and-mouse-shortcuts.html)

[Pycharm external tools instructions](https://www.jetbrains.com/help/pycharm/configuring-third-party-tools.html#pylint-configure)

[Pycharm configure keyboard shortcut](https://www.jetbrains.com/help/pycharm/configuring-keyboard-and-mouse-shortcuts.html)

## Add config files
Config files allow you to
* add additional directories to your python path during a test run
* customize the generated tests' root directory
* a python function to run before a test run to
    * configure aliases for frequently used inputs such as a full package name
    * patch dependencies of your test target

By default, it looks for a configuration file named test-scribe-config.yml in the working directory
of a test run. The config file's path can be overwritten with command line options.
[Here](https://github.com/HappyRay/testscribe/blob/main/test-scribe-config.yml) is a sample config file.

See [the config file](#configuration-file-format) section for more details.

# Configuration File Format
It's a [YAML](https://en.wikipedia.org/wiki/YAML) file.

## Add additional directories to the Python path for a test run 
example:

    python-paths:
    - src
    - tests

## Output files root directory
The value has to be an existing directory. 

example:

    output-root-dir: tests/generated

## A python function to run before a test run
The value has to be a fully qualified Python function name.

example:

    setup-function: setup.setup

setup is a function defined in the module named setup.
[Here](https://github.com/HappyRay/testscribe/blob/main/tests/setup.py) 
is an example of such a function.

# Input Support
## Expression
Valid Python expressions are supported as inputs.
Use fully qualified type names where a type is expected. 
For example: 
If you want to use a helper function called "get_test_val" in the module "tests.helper" to generate an input value,
you should use "tests.helper.get_test_val()" expression when prompted.

Tip:

Use the alias support to reduce the need to type long names.

## Create a real class instance
You can use the normal constructor expression to create an instance of a class for inputs.
For example: data.Person(name="Alice", age=23)

If the input is a class instance and is properly annotated, 
the class name can be replaced by a builtin alias named "c".
For example:
Given the following target
```python
from data import Person
def foo(p: Person):
  ...
```
You can simply use c(name="Alice", age=23) when prompted for the value of the parameter p.

[Here](demo.markdown#create-class-instance) is a demo.

[here](demo.markdown#objects-in-list) is a demo of creating objects in a list.

## Create a mock
You can also use the m function to create a mock object as an input.
If the type information is available to the tool, a builtin alias "m" may be used instead to
create a mock object of the given type with the default name.

Given the same foo function above, you can create a mock object of the type Person when prompted
for the p parameter by typing "m(data.Person)". Because the type information is available, you may
simply type "m" to create the same mock object.

See [the "m" function definition](https://github.com/HappyRay/testscribe/blob/main/src/testscribe/api/mock_api.py) 
for more information.

When a mock object's attributes are accessed for the first time, you will be prompted for their values.
When a mock object's method is called, the tool will show the parameters and the call stack. It will prompt
you for the return value.

[Here](demo.markdown#mock-class-instance) is a demo.

[here](demo.markdown#objects-in-list) is a demo of mocking multiple objects in a list.

# Commands

## Create a test run

```text
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
```
# Update test
```text
Usage: testscribe update [OPTIONS] SCRIBE_FILE_PATH TEST_NAME                  
                                                                                
 :param test_name: :param scribe_file_path: :return:                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    scribe_file_path      FILE  The testscribe file to update               │
│                                  [default: None]                             │
│                                  [required]                                  │
│ *    test_name             TEXT  The name of the test to update              │
│                                  [default: None]                             │
│                                  [required]                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```

# Delete a test 
```text
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

```
# Move tests
The generated test files are organized the same way as the module hierarchy.
When target functions' modules are changed, this command makes it easier to move the 
corresponding tests.

```text
 Usage: testscribe move [OPTIONS] SOURCE_FILE CLASS_OR_FUNCTION_NAME            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    source_file                 FILE  The source file that contains the     │
│                                        symbol                                │
│                                        [default: None]                       │
│                                        [required]                            │
│ *    class_or_function_name      TEXT  The name of the function or class     │
│                                        that has moved. To move tests for     │
│                                        methods, use the class name of the    │
│                                        methods.                              │
│                                        [default: None]                       │
│                                        [required]                            │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --config-file        FILE  The config file [default: None]                   │
│ --help                     Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

# Sync tests
Regenerate the unit test file to match the given TestScribe file.

```text
Usage: testscribe sync [OPTIONS] SCRIBE_FILE_PATH

:param scribe_file_path: :return:

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    scribe_file_path      FILE  The testscribe file to sync [default: None] │
│                                  [required]                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```

# Sync All
Sync all tests under the configured output root directory
```text
 Usage: testscribe sync-all [OPTIONS]                                           
                                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --config-file        FILE  The config file [default: None]                   │
│ --help                     Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯

```
