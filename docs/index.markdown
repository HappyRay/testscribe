---
layout: my-home
title: home
---
TestScribe, a tool to make python unit testing easier by automating the boring and repetitive parts.

Table of Contents
=================

* [The idea](#the-idea)
* [Quick start](#quick-start)
* [Command line help](#command-line-help)
* [Required setup](#required-setup)
* [Optional setup](#optional-setup)
    * [Quick launch for the Intellij/Pycharm IDE](#quick-launch-for-the-intellijpycharm-ide)
        * [An example intellij external tool configuration for the create command](#an-example-intellij-external-tool-configuration-for-the-create-command)
        * [References](#references)
    * [Add config files](#add-config-files)
* [Configuration File Format](#configuration-file-format)
    * [Add additional directories to the Python path for a test run](#add-additional-directories-to-the-python-path-for-a-test-run)
    * [Output files root directory](#output-files-root-directory)
    * [Setup function](#setup-function)
* [Test a method](#test-a-method)
* [Input Support](#input-support)
    * [Default value](#default-value)
    * [String](#string)
    * [Expression](#expression)
    * [Create a real class instance](#create-a-real-class-instance)
    * [Create a mock](#create-a-mock)
    * [Raise an exception for a mock call](#raise-an-exception-for-a-mock-call)
    * [Ignore the return value for a mock call](#ignore-the-return-value-for-a-mock-call)
    * [Input alias](#input-alias)
* [Test name](#test-name)
* [Patch](#patch)
* [Commands](#commands)
    * [Create a test run](#create-a-test-run)
    * [Update test](#update-test)
    * [Delete a test](#delete-a-test)
    * [Move tests](#move-tests)
    * [Sync tests](#sync-tests)
    * [Sync All](#sync-all)
* [Wrapper function](#wrapper-function)
* [Tips](#tips)
    * [Better output format in color](#better-output-format-in-color)
    * [Better string readability in the tscribe file](#better-string-readability-in-the-tscribe-file)
    * [Annotate instance member variables with type information](#annotate-instance-member-variables-with-type-information)
* [Debug logging](#debug-logging)
* [Limitations and possible workaround](#limitations-and-possible-workaround)
  * [Expression with both mocks and objects](#expression-with-both-mocks-and-objects)
* [FAQ](#faq)
    * [Do you have real world examples?](#do-you-have-real-world-examples)

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

Notice that the program can't be testscribe. The wrapper script is not available to the external program system.

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
The directories are relative to the configuration file location where they are defined. 
example:

    python-paths:
    - src
    - tests

The directories (config directory)/src and (config directory)/tests are added to the Python path 
for a test run.

## Output files root directory
The value has to be an existing directory. 

example:

    output-root-dir: tests/generated

## Setup function
Specifies a python function to run before a test run
The value has to be a fully qualified Python function name.

example:

    setup-function: setup.setup

setup is a function defined in the module named setup.
[Here](https://github.com/HappyRay/testscribe/blob/main/tests/setup.py) 
is an example of such a function.

# Test a method
When the target function is a method of a class, the tool will automatically call the constructor
to create an instance first and invoke the method on that instance.

[Here](demo.markdown#test-a-method) is a demo

In the rare case when there is at least another function or method in the same module with the same name,
you may create a wrapper function which creates an instance and invoke the method. You can then test
the wrapper function as usual.

# Input Support
## Default value
When prompted for an input, the default input is displayed. It's the string enclosed in [ ].
Press the return key will select the default input.

For example:

    Please provide the value for the parameter (a) of type: (int) [1]:

The default value above is 1.

[ ] means the default is an empty string.

## String
If the tool can infer from the type annotation that the input is a string,
the input doesn't need to be quoted. 
The inferred type information is displayed when prompting for inputs.
For example:
<pre>Please provide the value for the parameter (keyword) of type: <strong>(str)</strong> []: Bob</pre>
It indicates the inferred type is "str".

The quoted form is also accepted. 
In the example above the input ***"Bob"*** will provide the same string value Bob to the parameter.

The quoted form is needed when the string value contain special values that need to 
be quoted. For example: 
* to input multiline string use ***"a\nb"*** or ***'a\nb'***.
* to input **"** use **'"'**.

## Expression
Valid Python expressions are supported as inputs.
Use fully qualified type names where a type is expected. 
For example: 
If you want to use a helper function called "get_test_val" in the module "tests.helper" to generate an input value,
you should use "tests.helper.get_test_val()" expression when prompted.

Tip:

Use the [alias support](#input-alias) to reduce the need to type long names.

## Create a real class instance
You can use the normal constructor expression to create an instance of a class for inputs.
For example: data.Person(name="Alice", age=23)

If the input is a class instance and is properly annotated, 
the class name can be replaced by a builtin alias named "c".
For example:
Given the following target
```
from data import Person
def foo(p: Person):
  ...
```
You can simply use c(name="Alice", age=23) when prompted for the value of the parameter p.

[Here](demo.markdown#create-a-class-instance) is a demo.

[here](demo.markdown#multiple-class-instances-in-a-list) is a demo of creating objects in a list.

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

[Here](demo.markdown#mock-a-class-instance) is a demo.

[here](demo.markdown#multiple-class-instances-in-a-list) is a demo of mocking multiple objects in a list.

## Raise an exception for a mock call
To raise an exception for a mock call, use the builtin [throw](https://github.com/HappyRay/testscribe/blob/09f1e110dc03b357400226e3ac8f88153113d5a7/src/testscribe/api/mock_api.py#L25) 
function. 
For example: use ***throw(Exception("failed"))*** when prompted for a mock call return value.

[Here](demo.markdown#raise-an-exception-in-a-mock-call) is a demo.

## Ignore the return value for a mock call
If a mocked method call's return value is not used, it is sometimes simpler to just ignore it.

Use the special input string ***ignore*** when prompted for such a return value.

[Here](demo.markdown#ignore-the-return-value-of-a-mock-call) is a demo.

## Input alias
To reduce the amount of typing, aliases can be defined per test run.
They will be expanded to the full string before the input expression is evaluated.

Use the [define_alias](https://github.com/HappyRay/testscribe/blob/main/src/testscribe/api/alias.py)
function in a [setup function](#setup-function).

For example, you can define an alias for a frequently used package like this
> define_alias(alias="p2", full_str="tsdemo.package1.package2")

You can then use **p2** instead of the full package name for the test runs that use this setup function. 

For example:
> p2.Person

Multiple aliases can be defined and used in one expression. They are expanded in the order 
in which they are defined.

[Here](demo.markdown#input-alias) is a demo.

# Test name
You can provide a test name or take the default.

The default test name is the target function name.

Upper cases will be converted to lower cases.
The spaces in the name will be converted to _.
Camel cases will be converted to snake cases.

For example, an input of ***NegativeInput Should fail*** will be translated to 
***negative_input_should_fail***.

The tool will ensure each test in the same file has a unique name
 by appending a number with a leading _ when necessary.

Don't add ***test_*** prefix. It will be added automatically for the generated unit tests.

Use a leading '_' to include the target function name as part of the prefix.

For example, an input of ***_Positive input*** for a function foo will be translated to 
test_foo_positive_input in the generated unit tests. In the scribe files the test name will
 be _positive_input. This way when the target function name is changed, the tool can 
automatically regenerate the correct unit test names the next time the unit test file is generated.

# Patch
When a dependency is hard coded in the target function, you may need to patch it.
See the Python mock library documentation and [the realpython site](https://realpython.com/python-mock-library/) 
for more background information.

Use the 
[patch_with_mock or patch_with_expression functions](https://github.com/HappyRay/testscribe/blob/main/src/testscribe/api/mock_api.py) 
to instruct the tool to patch before the target function is executed. 

One way is to 
use [the setup function feature](#). Invoke these functions in a setup function you define for a test 
run. Remember to comment out or remove these calls for test runs to which these patches don't apply.

Alternatively you may create a wrapper function to call these functions before calling the target function.
And then use the tool to test the wrapper function.

[Here](demo.markdown#patch-a-function) is a demo for patching with a mock.

[Here](demo.markdown#patch-a-string) is a demo for patching with an expression.

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
## Update test
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

## Delete a test 
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
## Move tests
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

## Sync tests
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

## Sync All
Sync all tests under the configured output root directory
```text
 Usage: testscribe sync-all [OPTIONS]                                           
                                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --config-file        FILE  The config file [default: None]                   │
│ --help                     Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯

```

# Wrapper function
For more flexibility, you can create wrapper functions which call the target function.
Use the tool to test the wrapper functions.

Example scenarios when a wrapper function may be useful:
* Test a magic method such as __str__. [Here](demo.markdown#wrapper-function) is a demo.
* Use code to set up the preconditions before invoking the target function
* Additional verification of the output. For example, check if a file is indeed created.

[Here](https://github.com/HappyRay/testscribe/tree/main/tests/wrapper) are some example wrapper
functions used by the TestScribe project to test itself.

Since these wrapper functions are typically used for testing only, you may put them in a
test folder if you have one.

# Tips

## Better output format in color

Add [the rich library](https://github.com/Textualize/rich) as a dev dependency.

## Better string readability in the tscribe file
Prefer double quotes over single quotes to quote strings in inputs when needed.
Since YAML quotes strings with single quotes, it results in
a more readable YAML representation of strings in the tscribe files.

## Annotate instance member variables with type information
Proper type information makes input easier in some cases. 
Since instance member variables are created dynamically, it requires special techniques to
annotate them with type information.
To annotate, create a class variable with the type annotation.

For example:

```python
class Car:
    model: str

    def __init__(self, model: str):
        self.owner = owner
```

[Here](demo.markdown#annotate-a-class-instance-member-variable-with-type-information) 
is an example with a test run result.

# Debug logging
To gather additional debug information, put a file named test_scribe_logging.conf in
the working directory.
This is useful when reporting an issue for example.

[Here](https://github.com/HappyRay/testscribe/blob/main/test_scribe_logging.conf) is a sample config file.

See [the Python documentation](https://docs.python.org/3/library/logging.config.html#logging-config-fileformat)
for how to customize this file.

# Limitations and possible workaround

## Expression with both mocks and objects
For example 
> ((m(test_data.simple.C), test_data.simple.C())

The generated test won't be correct. The displayed output is still correct however.

An alternative is to create a wrapper function. For example:
foo_wrapper(o: test_data.simple.C)
And use (o,  test_data.simple.C()) as input.


# FAQ

## Do you have real world examples?
The tool uses itself to test. You can see the many examples 
[here](https://github.com/HappyRay/testscribe/tree/main/tests)