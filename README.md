# TestScribe for Python - unit test made easier

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

# Easy to get started and setup
Adding testscribe to your development dependencies is all you need to start using the basic features.
Most of the features should be self-explanatory to developers.
Additional features such as launching the tool more easily only require simple setups. 

# Low risk to try
* The tool doesn't modify the code you test in any way.
* It doesn't introduce any dependency to your production code.
* At any time, removing the tool won't break your existing production code or tests.
* It's free and open source with the Apache 2.0 license.
* You can always fall back to the traditional ways of testing for use cases the tool doesn't support yet. 
The tool won't get in your way.

# Demo
You can find demos [here](https://happyray.github.io/testscribe/demo.html).
Feel free to download the demo project and try for yourself.

# Documentation
It's capable of handling class instances, exceptions, class methods, mocking inputs, patching dependencies...
Please see the full documentation [here](https://happyray.github.io/testscribe/).

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
