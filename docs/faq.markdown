---
layout: my-home
title: FAQ
---
Frequently asked questions for [TestScribe](index.markdown)

Table of Contents
=================

* [Who is the tool designed for?](#who-is-the-tool-designed-for)
* [Can the tool help with integration testing?](#can-the-tool-help-with-integration-testing)
* [Are the generated tests valid if they always mirror the behavior of the code under test?](#are-the-generated-tests-valid-if-they-always-mirror-the-behavior-of-the-code-under-test)
* [Is this another test framework like pytest?](#is-this-another-test-framework-like-pytest)
* [Does it support test frameworks other than pytest such as unittest?](#does-it-support-test-frameworks-other-than-pytest-such-as-unittest)
* [Does it require me to change the way I write code?](#does-it-require-me-to-change-the-way-i-write-code)
* [Do you have real world examples?](#do-you-have-real-world-examples)
* [Can I modify the generated tests?](#can-i-modify-the-generated-tests)
* [Can I modify the scribe files?](#can-i-modify-the-scribe-files)
* [Is it better to keep only the scribe files for regression testing purposes?](#is-it-better-to-keep-only-the-scribe-files-for-regression-testing-purposes)
* [What to do if the tool doesn't support my use case?](#what-to-do-if-the-tool-doesnt-support-my-use-case)
* [Does the tool support programming languages other than Python?](#does-the-tool-support-programming-languages-other-than-python)
* [Can I still use it if I practice test-driven development](#can-i-still-use-it-if-i-practice-test-driven-development)
* [Will it increase the maintenance cost of tests](#will-it-increase-the-maintenance-cost-of-tests)
* [Does it support test parametrization in generated tests?](#does-it-support-test-parametrization-in-generated-tests)
* [Why is a mock annotated with the target type in the generated code](#why-is-a-mock-annotated-with-the-target-type-in-the-generated-code)

# Who is the tool designed for?
Please see [this section in the user guide](index.markdown#who-can-benefit-from-this-tool).

# Can the tool help with integration testing?
Yes if your test scenario can be covered by running a target function under the tool.
Since the cost of trying it is low, you can always try.

# Are the generated tests valid if they always mirror the behavior of the code under test?
You should only save the generated tests for regression test purpose **after** 
you verify visually the test result.

If the result is not what you expect, fix the code under test and update the test.
The [update test](#update-test) command makes it easier to update a test. 
You may use the generated test to debug the code under test if needed.

# Is this another test framework like pytest?
No. Typical test frameworks require you to **write** code in a certain way.
This tool doesn't require you to write code in most cases. 
Think of using this tool like a quick debugging session.
Thus, the investment is lower, and it's easier for you to stop using this tool 
without incurring much migration cost if you desire.

It does build on existing libraries such as the standard Python mock object library
and the pytest framework.

# Does it support test frameworks other than pytest such as unittest?
It currently only generates tests that uses the pytest framework. 

Maintaining pytest based tests in addition to the regular tests you have
may be easier than you may think because:
- the tests are generated
- you can [choose a different root directory](#output-files-root-directory) 
for the generated tests
- the generated tests use only the basic features of pytest, 
- if you don't plan to keep the generated tests for regression testing, you won't 
incur much of the maintenance cost of supporting another test framework. 

It's possible to extend it to support other test frameworks.

# Does it require me to change the way I write code?
No, it doesn't. It doesn't get in your way.

However, it gives you feedback to improve your code.
For example:
- It encourages you to annotate your code with type information since doing so makes it 
easier to provide inputs such as strings, mock objects.
- It encourages you to test more often and test earlier since the cost of doing so is much reduced.
- It gives you feedback about the quality of your code, testability, simplicity for example.

# Do you have real world examples?
The tool uses itself to test. You can see the many examples 
[here](https://github.com/HappyRay/testscribe/tree/main/tests).

The tool made it much easier to get high code coverage for about 3000 statements. 
See the latest code coverage report [here](https://app.codecov.io/gh/HappyRay/testscribe).

# Can I modify the generated tests?
Your changes will be overwritten if you update any test that the file contains using the tool.
You may copy the generated test and use it as you see fit.

# Can I modify the scribe files?
You can. However, it is not recommended. 

Some of your changes may be overwritten the next time the file is updated by the tool. 
For example, the tool will group the tests targeting the same function together.

It is often easier and less error-prone if you use one of [the commands](#commands) to do so.
These commands will also automatically regenerate the unit test files to keep them in sync with
the scribe files.

# Is it better to keep only the scribe files for regression testing purposes?
If the unit test files are generated from the scribe files, is it better to keep only the scribe files
for regression testing purposes?

It's a valid choice to keep only the scribe files and dynamically regenerate the unit test files 
for regression testing.

There are a number of advantages of keeping the unit test files:
- IDEs can index the test files. This allows you to find the tests for a target function more easily
for example.
- It's faster to run tests.
- Some readers of your tests may prefer reading the unit test files.

# What to do if the tool doesn't support my use case?
You can always fall back to the traditional ways of testing. The tool won't get in your way.
It may however provide examples, tests for further customization etc.
A wrapper function may be used to provide partial help. For example help with generating the 
test file and test function while leaving the bulk of the work to the wrapper function.

# Does the tool support programming languages other than Python?
Not currently. However, the same technique can be applied to other languages.

# Can I still use it if I practice test-driven development
If you are willing to adjust your workflow a little, the tool can still help you. 

Here is one possible workflow:
1. Write the minium production code to satisfy the contract.
2. Use the tool to generate a test which would be the same test you would have to write manually before.
3. Continue with your workflow as before.

An example minium production code for a contract like "given an integer customer id return a customer name":
```python
def get_customer_name(customer_id: int):
    return "Bob"
```

Use the tool to generate a test with the customer Bob's id. 
Now progress towards the real implementation. The first test for Bob should still pass. 
Test again using the tool with a different customer's id to generate additional tests.

# Will it increase the maintenance cost of tests
You can choose which generated tests to keep. And the tool can help manage the generated tests you keep.

For example:
* [Move tests](#move-tests) after the target functions are moved.
* [Update tests](#update-test) is often easier than creating a new test since it can use the existing input as default.

It's true that the generated tests are strict. If you prefer, you can make a copy of the generated test and 
change it as you see fit. It's often easier than creating the same test manually.
Given how easy it is to update tests if only the output has changed,
it is often easier to update a test than relaxing assertions.
And it serves as an additional safeguard.

# Does it support test parametrization in generated tests?
pytest supports [test parametrization](https://docs.pytest.org/how-to/parametrize.html#parametrize-basics)
to allow one test to take different set of inputs.

This tool only generates tests that test one set of input each. The amount of work you have to 
do is similar or less, in part thanks to the intelligent selection of default input values. 
After all, you will need to input all the input data either way. 
With the tool, you can focus on the input data itself 
without having to remember the syntax and type in the extra code to make pytest parametrization work 
,not to mention creating a test file, importing modules and writing other boilerplate code.
As a bonus, if the production code has the proper type annotation for string inputs, 
you don't even need to quote the input string.

The approach has the following additional benefits:
* The generated test is easier to read when one would like to focus on one set of input. 
When the input becomes more complex, nested lists for example, the parameterized tests become harder to read.
* It's easier to test/debug a single set of input.
* You have the ability to give each test for each input set its own descriptive name and description.

Test parametrization makes more sense when tests are written manually to reduce code duplication.
With this tool, some code duplication is ok since the duplicated part is handled by the tool without requiring extra 
effort from you.

[Here](demo.markdown#test-multiple-input-sets) is an example that you can see/try for yourself.

# Why is a mock annotated with the target type in the generated code
This makes it easier to find where this type is used.
