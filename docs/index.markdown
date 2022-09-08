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
