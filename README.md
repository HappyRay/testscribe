# TestScribe for Python

Unit test made easy

A tool to make python unit testing easier by automating the boring and repetitive parts.

# A simple example

Here is a very basic simple example to illustrate the basic usage.
Suppose you have a function called is_prime in the file testscribe_test/prime.py. It checks if the input
number is a prime number. You can unit test the function using TestScribe without writing any boilerplate unit test code 
as follows:

    (.venv)[~/code/testscribe-test (main *)]$ testscribe create testscribe_test/prime.py is_prime
    ...
    Please provide the value for the parameter (n) of type: (int) []: 8
    Calling is_prime(n=8)
    ***** Result:
    type: <class 'bool'>
    value:
    False
    ***** Result end
    ...
    Wrote the generated test file to: /home/ray/code/testscribe-test/tests/generated/testscribe_test/test_prime_g.py
