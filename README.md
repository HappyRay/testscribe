# TestScribe for Python

Unit test made easy

A tool to make python unit testing easier by automating the boring and repetitive parts.

# A simple example

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

You can run it multiple times with different inputs.

TestScribe automatically creates fully functional unit test files. You can use them to debug a test run or save
them as regression tests or simply discard them. 

The example above generates the following test file test_prime_g.py
    
    from prime import is_prime
    def test_is_prime():
        result = is_prime(n=8)
        assert result is False

This is the code you would likely have to write to unit test the same without TestScribe's help.