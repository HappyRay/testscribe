---
layout: my-home
title: home
---
TestScribe, a "low code/no code" command line tool to make python testing easier by automating the boring and repetitive parts.

## Tips for navigating this guide
If you prefer learning by watching the tool in action, start with [a simple demo](#a-simple-example) 
and [more demo videos](#demo-videos).

If you prefer reading first to figure out if the tool is for you, start with [the introduction](#introduction)
followed by [the idea](#the-idea), [Who can benefit from this tool](#who-can-benefit-from-this-tool) 
sections.

If you prefer trying it with minimum effort, start with [the quick start](#quick-start).

You don't need to learn all the details at once. Refer to the documentation when your need for a specific feature
arises. It's helpful to browse the document or the table of content to learn what it covers.

Table of Contents
=================

* [Introduction](#introduction)
  * [A simple example](#a-simple-example)
  * [Demo](#demo)
    * [Demo videos](#demo-videos)
  * [Easy to get started and setup](#easy-to-get-started-and-setup)
  * [Low risk to try](#low-risk-to-try)
  * [Frequently asked questions](#frequently-asked-questions)
* [The idea](#the-idea)
* [Who can benefit from this tool?](#who-can-benefit-from-this-tool)
  * [Developers who write unit tests but don't like the overhead](#developers-who-write-unit-tests-but-dont-like-the-overhead)
  * [Developers who don't write unit tests](#developers-who-dont-write-unit-tests)
  * [Casual Python users who don't know unit tests well](#casual-python-users-who-dont-know-unit-tests-well)
* [Minimum requirement](#minimum-requirement)
* [Quick start](#quick-start)
* [Command line help](#command-line-help)
* [Python module search path](#python-module-search-path)
* [Required setup](#required-setup)
* [Optional setup](#optional-setup)
  * [Quick launch for the Intellij/Pycharm IDE](#quick-launch-for-the-intellijpycharm-ide)
    * [An example intellij external tool configuration for the create command](#an-example-intellij-external-tool-configuration-for-the-create-command)
    * [References](#references)
  * [Quick launch for the Visual Studio Code IDE](#quick-launch-for-the-visual-studio-code-ide)
    * [Prevent the auto activation of the Python environment](#prevent-the-auto-activation-of-the-python-environment)
    * [An example VS Code configuration for the create command](#an-example-vs-code-configuration-for-the-create-command)
    * [Configure keyboard shortcut](#configure-keyboard-shortcut)
  * [Add config files](#add-config-files)
    * [Add additional directories to the Python module search path for a test run](#add-additional-directories-to-the-python-module-search-path-for-a-test-run)
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
* [Customize how class instances are displayed and asserted](#customize-how-class-instances-are-displayed-and-asserted)
* [Wrapper function](#wrapper-function)
* [Scribe files](#scribe-files)
* [Assertion of complex objects](#assertion-of-complex-objects)
* [Tips](#tips)
  * [Better output format in color](#better-output-format-in-color)
  * [Better string readability in scribe files](#better-string-readability-in-scribe-files)
  * [Annotate instance member variables with type information](#annotate-instance-member-variables-with-type-information)
* [Debug logging](#debug-logging)
* [Limitations and possible workaround](#limitations-and-possible-workaround)
  * [Expression with both mocks and objects](#expression-with-both-mocks-and-objects)
  * [Unsupported python features](#unsupported-python-features)
* [Project page](#project-page)
* [How to engage the user community](#how-to-engage-the-user-community)
  * [Google group for discussions](#google-group-for-discussions)
  * [Stackoverflow for questions](#stackoverflow-for-questions)
  * [GitHub for reporting issues or feature requests](#github-for-reporting-issues-or-feature-requests)
  * [Social media](#social-media)
* [Copyright and license](#copyright-and-license)

# Introduction
Do you wish you don't have to write expected results in code but just visually verify the
result just like you would with testing a web page?

Do you write unit tests but don't like the overhead (create a file, name a function, write assertions...)
or repetitiveness?

Have you experienced adjusting the mocking code multiple times before it allows the test to run?
Do you have to refer to documentation from time to time to figure out how to mock or assert complex
mock call parameters?

Do you wish to start a debugging session to understand a function better
with as little overhead as possible?

Are you looking for an intuitive tool to help improve your code and coding skills?

This tool can help. It will
- ask for inputs only and show you the test result.
- take care of the repetitive and boring part of unit testing such as invoking the target function,
  creating files and functions with proper conventions, generating the assertions...
- interactively prompt for the mock object's behavior in context with information such as the call stack.
- generate complete working test code, which can serve as regression tests, examples and basis
  for further customization.
- and more. It's capable of handling class instances, exceptions, class methods, mocking inputs, 
patching dependencies... Please see the rest of this document for more details.

## A simple example

Here is a very basic simple example to illustrate the basic usage.
Suppose you have a function called is_prime in a file prime.py. It checks if the input
number is a prime number. You can unit test the function using TestScribe without writing any boilerplate
unit test code as follows:

    $ testscribe create prime.py is_prime
    ...
    Please provide the value for the parameter (n) of type: (int) []: 8
    Calling is_prime(n=8)
    ***** Result:
    type: <class 'bool'>
    value:
    False
    ***** Result end

Notice the only input you need to provide is the number 8.

You can run it multiple times with different inputs and inspect the displayed output.
If the output is not correct, fix the production code and test again.

TestScribe automatically creates fully functional unit test files. You can use them to debug a test run or save
them as regression tests or simply discard them.

The example above generates the following test file test_prime_g.py

    from prime import is_prime
    def test_is_prime():
        result = is_prime(n=8)
        assert result is False

This is the code you would likely have to write to unit test the same without TestScribe's help.

Below is a short demo video for the example above.

{% include youtube.html id="bMAyXsd8yAw" %}

The benefits will become more significant for more complex scenarios.
[Here](demo.markdown#mock-a-class-instance)
is an example involving mocks with another demo video.

## Demo
You can find more demos [here](demo.markdown).
Feel free to download the demo project and try for yourself.

### Demo videos
* [Mock a class instance](demo.markdown#mock-a-class-instance)
* [A real-world example of an end-to-end test scenario and how to update it](demo.markdown#a-real-world-example-of-an-end-to-end-test-scenario-and-how-to-update-it)
* [Compare testing with the TestScribe testing tool with the traditional test method](demo.markdown#test-multiple-input-sets) 

## Easy to get started and setup
Adding testscribe to your development dependencies is all you need to start using the basic features.
Most of the features should be self-explanatory to developers.
Additional features such as launching the tool more easily only require simple setups.

## Low risk to try
* The tool doesn't modify the code you test in any way.
* It doesn't introduce any dependency to your production code.
* At any time, removing the tool won't break your existing production code or tests.
* It's free and open source with the Apache 2.0 license.
* You can always fall back to the traditional ways of testing for use cases the tool doesn't support yet.
  The tool won't get in your way.

## Frequently asked questions
Have questions before diving into details? You may find answers at the [FAQ page](faq.markdown)

# The idea
Unit tests should be as intuitive as testing a web page. 
Developers should be able to test a function by providing inputs **interactively** and 
verify outputs **visually** without having to write boilerplate code in most cases. 
The process is similar to a debugging session which answers
"what happens when I pass this input". 
Note that 
* mock objects' attributes and mock methods' return values are inputs
* parameter values to mock method calls are outputs

Additionally, the test runs are recorded both as traditional unit tests 
and files in a structured machine-readable format by the tool automatically.
The machine-readable format will enable additional functionalities such as maintaining 
regression tests.

The machine-readable files are referred to as [scribe files](#scribe-files) in the documentation.

# Who can benefit from this tool?
All the Python developers can benefit from this tool in ways as they see fit.

Here are some example profiles:

## Developers who write unit tests but don't like the overhead
The tool frees you from the boring and repetitive parts of testing and allows you to focus on
the intellectually stimulating parts such as designing the test scenarios and verifying the output.

You may discover/rediscover the fun of unit testing with the help of this tool.

## Developers who don't write unit tests
You may find the tool helpful on occasions when you need to quickly verify the behavior
of your own code or some library or code someone else write. 

For example, you may use this tool to test a code path, such as an error handling code,
that is not easily invoked in an integration test. 

Note that you don't have to use the generated test code if you don't need or want to.

## Casual Python users who don't know unit tests well
It will be another tool in your toolbox. It is not difficult to learn. It can introduce you 
to the power of unit testing without a big commitment or a steep learning curve.
You don't have to learn up front how to describe a mock object's behavior in code for example.
You can use the generated tests as examples to learn gradually how to write unit tests yourself.

For example, data scientists or analyst or IT admins may use this tool to test some components of scripts
to avoid wasting time discovering simple errors after the script is deployed, maybe to a large
computing cluster. 

You don't have to use the generated test files for regression testing, although
you may find regression testing as a bonus later on.

# Minimum requirement
* Python version >= 3.7.

# Quick start

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
The tests are based on the [pytest](https://docs.pytest.org/) test framework.

# Command line help
Use the --help option to display help information from a command line.

    testscribe --help

output:

    Usage: testscribe [OPTIONS] COMMAND [ARGS]...

Use the --help option after a command name to display help information
for that command.

For example:

    testscribe create --help

# Python module search path
Without [a configuration file](#add-config-files), the current working directory is appended to 
the Python module search path which is accessible in the Python variable sys.path.

With a configuration file, the configuration file directory is appended to the search path
in addition to 
[the additional directories you configure](#add-additional-directories-to-the-python-module-search-path-for-a-test-run). 

# Required setup
Use your favorite tool to add [testscribe](https://pypi.org/project/testscribe/) to your development python 
library dependencies. Note that it is not needed as a production dependency.

If you would like to take advantage of the generated tests, add [pytest](https://docs.pytest.org/) to 
your development python library dependencies too.

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

## Quick launch for the Visual Studio Code IDE
Visual Studio code IDE can be configured to launch the tool more easily and quickly.

### Prevent the auto activation of the Python environment
Add the following config to the settings.json file

"python.terminal.activateEnvironment": false

Without it, the program may incorrectly receive the activation message as the first input.

### An example VS Code configuration for the create command
Add to the tasks.json file in the .vscode folder
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Create TestScribe tests",
            "type": "process",
            "command": "${command:python.interpreterPath}",
            "args": ["-m", "testscribe", "create", "${file}", "${selectedText}"],
            "group": {
                  "kind": "test"
              },
              "presentation": {
                  "reveal": "always",
                  "focus": true
              }
          }
    ]
}
```
If the task fails to launch and the output window shows an error related to the 
python command path, change the command value to a relative path to the python executable
your project is using as a workaround.
For example:
"command": ".venv\\Scripts\\python.exe",

To test a function, open the target file, highlight the function to test, invoke the configured task.

Other commands can be configured in a similar way.

Notice that the program can't be testscribe. The wrapper script is not available outside the activated environment.

Reference:

[Integrate with External Tools via Tasks](https://code.visualstudio.com/docs/editor/tasks)

### Configure keyboard shortcut
It's helpful to configure keyboard shortcuts to launch the tasks defined above.

Here is an example for launching the create test command task defined above.

Add to [the keybindings.json file](https://code.visualstudio.com/docs/getstarted/keybindings#_advanced-customization)
```json
[
    {
        "key": "ctrl+shift+q",
        "command": "workbench.action.tasks.runTask",
        "args": "Create TestScribe tests",
        "when": "editorTextFocus"
    }
]
```
Reference:
[Configure key bindings for tasks](https://code.visualstudio.com/docs/editor/tasks#_binding-keyboard-shortcuts-to-tasks)

## Add config files

It's a [YAML](https://en.wikipedia.org/wiki/YAML) file.

By default, it looks for a configuration file named test-scribe-config.yml in the working directory
of a test run. The config file's path can be overwritten with command line options.

[Here](https://github.com/HappyRay/testscribe/blob/main/test-scribe-config.yml) is a sample config file.

The directory values in the configuration file are relative to the configuration file location
where they are defined.

The configuration file support the following configurations.

### Add additional directories to the Python module search path for a test run
See [the Python module search path](#python-module-search-path) section for the default behavior.

For example:

    python-paths:
    - src
    - tests

The directories (config directory)/src and (config directory)/tests are appended to the Python module search path
in addition to the directory of the configuration file
for a test run that uses this configuration file.

### Output files root directory
Default: a directory named test_scribe_tests in the current working directory.

If the directory doesn't exist, it will be created.

example:

    output-root-dir: tests/test_scribe_tests

### Setup function
Specifies a python function to run before a test run
The value has to be a fully qualified Python function name.

example:

    setup-function: setup.setup

setup is a function defined in the module named setup.

Use the setup function to:

* configure [aliases](#input-alias) for frequently used inputs such as a full package name
* [patch](#patch) dependencies of your test target

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
use [the setup function feature](#setup-function). Invoke these functions in a setup function you define for a test 
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
Usage: testscribe update [OPTIONS] FILE_PATH TEST_NAME                         
                                                                                
 Update the selected test.                                                      
 :param test_name: :param file_path: :return:                                   
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    file_path      FILE  The scribe file or test file to update             │
│                           [default: None]                                    │
│                           [required]                                         │
│ *    test_name      TEXT  The name of the test to update [default: None]     │
│                           [required]                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Delete a test
```text
Usage: testscribe delete [OPTIONS] FILE_PATH TEST_NAME                         
                                                                                
 Delete a test. This will delete the test from both the scribe file and the     
 unit test file.                                                                
 :param file_path: :param test_name: :return:                                   
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    file_path      FILE  The scribe file or test file that contains the     │
│                           test to delete                                     │
│                           [default: None]                                    │
│                           [required]                                         │
│ *    test_name      TEXT  The name of the test to delete [default: None]     │
│                           [required]                                         │
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
Regenerate the unit test file to match the given scribe file.

```text
 Usage: testscribe sync [OPTIONS] FILE_PATH                                     
                                                                                
 Regenerate the unit test file.                                                 
 :param file_path: :return:                                                     
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    file_path      FILE  The scribe file or test file to sync               │
│                           [default: None]                                    │
│                           [required]                                         │
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

# Customize how class instances are displayed and asserted
If the class doesn't implement a custom \_\_repr\_\_ method, 
the result display and generated assertions will be based on member fields.
[Here](demo.markdown#the-class-doesnt-implement-a-custom-repr-method) is a demo.

If it does, the result display and generated assertions will be based on the result of repr(object).
[Here](demo.markdown#the-class-implements-a-custom-repr-method) is a demo.
This way you can have some control. You can exclude some member fields for example.
The generated assertions are typically more compact.

# Wrapper function
For more flexibility, you can create wrapper functions which call the target function.
Use the tool to test the wrapper functions.

Example scenarios when a wrapper function may be useful:
* Test a magic method such as __str__. [Here](demo.markdown#wrapper-function) is a demo.
* Use code to set up the preconditions before invoking the target function
* Additional verification of the output. For example, check if a file is indeed created.
* Test a scenario which is not covered by an existing function. 
e.g. test pushing one item to a stack and popping it twice. 

[Here](https://github.com/HappyRay/testscribe/tree/main/tests/wrapper) are some example wrapper
functions used by the TestScribe project to test itself.

Since these wrapper functions are typically used for testing only, you may put them in a
test folder if you have one.

# Scribe files
The tool generates machine-readable [YAML](https://en.wikipedia.org/wiki/YAML) formatted files 
with the tscribe extension alongside the unit test files.
They are referred to as scribe files in the documentation.
The [sync tests command](#sync-tests) and the [sync all](#sync-all) command generate unit test files
based on the corresponding scribe files.

[Here](demo.markdown#scribe-files) are scribe file demos.

See the [FAQ](faq.markdown) for more information related to the scribe files.

# Assertion of complex objects
The tool automatically generates assertion for complex mock call parameters such as
class instances. This would be cumbersome to do manually.
[Here](demo.markdown#assert-class-instances-in-mock-call-parameters) is a demo.

# Tips

## Better output format in color

Add [the rich library](https://github.com/Textualize/rich) as a dev dependency.

## Better string readability in scribe files
Prefer double quotes over single quotes to quote strings in inputs when needed.
Since YAML quotes strings with single quotes, it results in
a more readable YAML representation of strings in scribe files.

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
        self.model = model
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

The generated test won't be correct. The displayed output is still correct, however.

An alternative is to create a wrapper function. For example:
foo_wrapper(o: test_data.simple.C)
And use (o,  test_data.simple.C()) as input.

## Unsupported python features
Some Python features may not be supported yet. For example the async related features.
The command line output may still be useful even though the generated tests need to be discarded.
Try creating [wrapper test functions](#wrapper-function) as workarounds.
You can always fall back to traditional testing methods. 

# Project page
[Here](https://github.com/HappyRay/testscribe) is the project page.

# How to engage the user community

## Google group for discussions
Join [the Google group pyscribe@googlegroups.com](https://groups.google.com/g/pyscribe)

## Stackoverflow for questions
Include the text testscribe in the question to increase the chance that the question is answered.

## GitHub for reporting issues or feature requests
Open an issue at [the GitHub project](https://github.com/HappyRay/testscribe/issues).
Please only use this channel for reporting issues or suggesting a new feature.

## Social media
Use the tag #testscribe


# Copyright and license

Copyright 2022 Ruiguo (Ray) Yang

     Licensed under the Apache License, Version 2.0 (the "License");
     you may not use this file except in compliance with the License.
     You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

     Unless required by applicable law or agreed to in writing, software
     distributed under the License is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
     See the License for the specific language governing permissions and
     limitations under the License.
