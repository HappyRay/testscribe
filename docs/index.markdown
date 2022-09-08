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
verify outputs visually. Note that 
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
