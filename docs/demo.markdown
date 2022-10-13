---
layout: my-home
title: demo
---
Demonstrations of select features of [the TestScribe tool](https://github.com/HappyRay/testscribe).

Table of Contents
=================

* [Exception result](#exception-result)
* [Test a method](#test-a-method)
* [Test multiple input sets](#test-multiple-input-sets)
* [Mock a class instance](#mock-a-class-instance)
* [Create a class instance](#create-a-class-instance)
* [Multiple class instances in a list](#multiple-class-instances-in-a-list)
  * [Create multiple real instances in a list](#create-multiple-real-instances-in-a-list)
  * [Create multiple mocks in a list](#create-multiple-mocks-in-a-list)
* [Raise an exception in a mock call](#raise-an-exception-in-a-mock-call)
* [Ignore the return value of a mock call](#ignore-the-return-value-of-a-mock-call)
* [Patch a function](#patch-a-function)
* [Patch a string](#patch-a-string)
* [Input alias](#input-alias)
* [Wrapper function](#wrapper-function)
* [Annotate a class instance member variable with type information](#annotate-a-class-instance-member-variable-with-type-information)
* [Results that contain class instances](#results-that-contain-class-instances)
  * [The class doesn't implement a custom __repr__ method.](#the-class-doesnt-implement-a-custom-__repr__-method)
  * [The class implements a custom __repr__ method.](#the-class-implements-a-custom-__repr__-method)

[Here](https://github.com/HappyRay/testscribe-demo) is the demo project.
It's intentionally made as simple as possible to make it easier to understand.  
Feel free to download it and play with it.

For more realistic examples, see how the tool uses itself to test
[here](https://github.com/HappyRay/testscribe/tree/main/tests).

# Exception result
When a test run results in an exception, the tool can display the exception information and generate the 
appropriate test code.

This target function [always_raise_exception](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/raise_exception.py)
will always raise an exception.

An example test run output:

```text
...
Calling always_raise_exception()
The function always_raise_exception throws an exception.
Traceback (most recent call last):
  File "/home/ray/code/testscribe/src/testscribe/execution.py", line 86, in get_args_and_call
    ret_value = call_target_function(func, args)
  File "/home/ray/code/testscribe/src/testscribe/execution_util.py", line 87, in call_target_function
    return func(*binded_args.args, **binded_args.kwargs)
  File "/home/ray/code/testscribe-demo/tsdemo/raise_exception.py", line 7, in always_raise_exception
    raise Exception("test exception")
Exception: test exception
...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_raise_exception_g.py) 
is the generated test.

# Test a method
When the target function is a method of a class, the tool will automatically call the constructor
to create an instance first and invoke the method on that instance.

This method [greet](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/greet.py) is the target.

An example test run output:

```text
...
Prepare to create an instance of the class: Greeter
Getting parameters for the function (Greeter)
Please provide the value for the parameter (my_name) of type: (str) []: Bob
Calling Greeter(my_name='Bob')
Prepare to call the target function.
Getting parameters for the function (Greeter.greet)
Please provide the value for the parameter (to) of type: (str) []: Alice
Calling Greeter.greet(to='Alice')
***** Result:
type: <class 'str'>
value:
Hello Alice. My name is Bob
***** Result end
...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_greet_g.py)
is the generated unit test code.

# Test multiple input sets
See [this FAQ](index.markdown#does-it-support-test-parametrization-in-generated-tests) for the background information.

The [eval_expression](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/parametrization.py) function
takes an expression as a string and returns its evaluation result. We will test different expressions
with multiple test runs. Here are the test runs:

```text
...
Please provide the value for the parameter (expr) of type: (str) []: 3 + 5
Calling eval_expression(expr='3 + 5')
***** Result:
type: <class 'int'>
value:
8
***** Result end
Test name: [_]: _addition
...
```

```text
...
Please provide the value for the parameter (expr) of type: (str) [3 + 5]: 2 + 4
Calling eval_expression(expr='2 + 4')
***** Result:
type: <class 'int'>
value:
6
***** Result end
Test name: [_]: _addition
...
```

```text
...
Please provide the value for the parameter (expr) of type: (str) [2 + 4]: 6 * 9
Calling eval_expression(expr='6 * 9')
***** Result:
type: <class 'int'>
value:
54
***** Result end
Test name help: 'test_' prefix will be added automatically. Use a leading '_' to include the target function name as part of the prefix.
Test name: [_]: _multiplication
...
```

You only need to type in the expressions (3+5, 2+4, 6 * 9) and the test names (_addition, _multiplication).

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_parametrization_g.py) 
is the generated tests.

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/manual/test_parametrization.py) 
is the manually written test for comparison.

Try for yourself to see which method (manual vs using the tool) makes you and people who read your tests
more productive for this test.

# Mock a class instance
The function [search_name](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/simple_mock.py) takes a [Service](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/service.py) object as a parameter.
The service may involve a database or a network call.
It's easier to test by mocking it.

An example test run output:

```text
...
Please provide the value for the parameter (service) of type: (tsdemo.service.Service) []: m
Created a mock: Mock: name (m_service) spec (<class 'tsdemo.service.Service'>)
Please provide the value for the parameter (keyword) of type: (str) []: Bob
Calling search_name(service=Mock: name (m_service) spec (<class 'tsdemo.service.Service'>), keyword='Bob')
m_service's search_a_name method is called
with: keyword='key: Bob'.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/simple_mock.py", line 11, in search_name
    name = service.search_a_name("key: " + keyword)

Please provide the value for the return value of type: (str) []: real Bob
Mock call return value: 'real Bob'
***** Result:
type: <class 'str'>
value:
{"name": "real Bob"}
***** Result end
...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_simple_mock_g.py) 
is the generated unit test code.

# Create a class instance
The function [get_person_age](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/create_object.py) takes a 
[Person](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/person.py) object as a parameter.

An example test run output:

```text
...
Please provide the value for the parameter (p) of type: (tsdemo.person.Person) []: c("Bob", 10)
Calling get_person_age(p=tsdemo.person.Person("Bob", 10))
***** Result:
type: <class 'int'>
value:
10
***** Result end...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_create_object_g.py)
is the generated unit test code.

# Multiple class instances in a list
The function [get_average_age](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/objects_in_list.py) takes a
list of [Person](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/person.py) object as a parameter.

## Create multiple real instances in a list
An example test run:

```text
...
Please provide the value for the parameter (person_list) of type: (typing.List[tsdemo.person.Person]) []: [tsdemo.person.Person("a", 2), tsdemo.person.Person("b", 3)]
Calling get_average_age(person_list=[tsdemo.person.Person("a", 2), tsdemo.person.Person("b", 3)])
***** Result:
type: <class 'int'>
value:
2
***** Result end
...
```

## Create multiple mocks in a list

An example test run:
```text
Please provide the value for the parameter (person_list) of type: (typing.List[tsdemo.person.Person]) []: [m, m]
Created a mock: Mock: name (m_person) spec (<class 'tsdemo.person.Person'>)
Created a mock: Mock: name (m_person_1) spec (<class 'tsdemo.person.Person'>)
Calling get_average_age(person_list=[<testscribe.mock_proxy.MockProxy object at 0x7f43dd744af0>, <testscribe.mock_proxy.MockProxy object at 0x7f43dd744e50>])
Mock object m_person's ( age ) attribute is accessed for the first time.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/objects_in_list.py", line 12, in get_average_age
    total += p.age

Please provide the value for the age attribute of type: (int) []: 2
Mock attribute value: 2
Mock object m_person_1's ( age ) attribute is accessed for the first time.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/objects_in_list.py", line 12, in get_average_age
    total += p.age

Please provide the value for the age attribute of type: (int) []: 3
Mock attribute value: 3
***** Result:
type: <class 'int'>
value:
2
***** Result end
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_objects_in_list_g.py)
is the generated unit test code.

# Raise an exception in a mock call
The function [search_name](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/simple_mock.py) takes a [Service](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/service.py) object as a parameter.
The search_a_name method on that Service object is called.
An example test run output to test the behavior when the call throws an exception:

```text
...
Please provide the value for the parameter (service) of type: (tsdemo.service.Service) [m(tsdemo.service.Service, 'm_service')]: 
Created a mock: Mock: name (m_service) spec (<class 'tsdemo.service.Service'>)
Please provide the value for the parameter (keyword) of type: (str) [Bob]: 
Calling search_name(service=Mock: name (m_service) spec (<class 'tsdemo.service.Service'>), keyword='Bob')
m_service's search_a_name method is called
with: keyword='key: Bob'.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/simple_mock.py", line 11, in search_name
    name = service.search_a_name("key: " + keyword)

Please provide the value for the return value of type: (str) [real Bob]: throw(Exception("search failed"))
Mock call return value: InputValue(expression='throw(Exception("search failed"))', value=Exception('search failed'))
The function search_name throws an exception.
...
Exception: search failed

Test name help: 'test_' prefix will be added automatically. Use a leading '_' to include the target function name as part of the prefix.
Test name: [_]: _exception is propagated
...
```
Notice that this test run use an earlier test run's input as default input.

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_simple_mock_g.py)
is the generated unit test code.

# Ignore the return value of a mock call
The function [show](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/ignore_mock_return.py) takes a 
Printer object as a parameter.
The display method on that Printer object is called.
The returned string is not used by this function.
It's easier to ignore this return value when the object is mocked during a test.
And the generated test is simpler.

An example test run output to ignore the mocked display call:

```text
...
Please provide the value for the parameter (text) of type: (str) []: a
Please provide the value for the parameter (printer) of type: (tsdemo.ignore_mock_return.Printer) []: m
Created a mock: Mock: name (m_printer) spec (<class 'tsdemo.ignore_mock_return.Printer'>)
Calling show(text='a', printer=Mock: name (m_printer) spec (<class 'tsdemo.ignore_mock_return.Printer'>))
m_printer's display method is called
with: text='a'.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/ignore_mock_return.py", line 17, in show
    printer.display(text)

Please provide the value for the return value of type: (str) []: ignore
Mock call return value: InputValue(expression='ignore', value='Ignored')
...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_ignore_mock_return_g.py)
is the generated unit test code.

# Patch a function
The function [call_fixed_func](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/patch_function.py) has a 
fixed dependency on the calculate function. 

To replace the calculate function with a mock object for a test, add the following code to the setup function

    patch_with_mock(calculate)

The setup function definition is [here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/setup.py).
Uncomment the line before starting a test run which specifies this setup function. The configuration file is
[here](https://github.com/HappyRay/testscribe-demo/blob/main/test-scribe-config.yml) 

The setup function is called before the target function is called. The
[patch_with_mock](https://github.com/HappyRay/testscribe/blob/main/src/testscribe/api/mock_api.py) function
replaces the target function with a mock object of the same type as the target function. 

```text
...
Calling the setup function setup.setup.
setup function in tests is called.
Created a mock: Mock: name (m_calculate) spec (<function calculate at 0x7fe62436eb80>)
Patch tsdemo.patch_function.calculate with Mock: name (m_calculate) spec (<function calculate at 0x7fe62436eb80>)
Prepare to call the target function.
Getting parameters for the function (call_fixed_func)
Please provide the value for the parameter (num) of type: (int) []: 2
Calling call_fixed_func(num=2)
m_calculate is called
with: seed=2.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/patch_function.py", line 12, in call_fixed_func
    return calculate(num)

Please provide the value for the return value of type: (int) []: 1
Mock call return value: 1
***** Result:
type: <class 'int'>
value:
1
***** Result end
...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_patch_function_g.py)
is the generated unit test code.

# Patch a string
The function [get_db_name](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/patch_string.py) has a
fixed dependency on the DB_NAME variable.

To replace the string for a test, add the following code to the setup function

        patch_with_expression(target_str="tsdemo.patch_string.DB_NAME", expression="'test'")

Notice that the string value has to be quoted to be a valid Python expression.

The setup function definition is [here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/setup.py).
Uncomment the line before starting a test run which specifies this setup function.

Test run output:

```text
...
setup function in tests is called.
Patch tsdemo.patch_string.DB_NAME with 'test'
Prepare to call the target function.
Getting parameters for the function (get_db_name)
Calling get_db_name()
***** Result:
type: <class 'str'>
value:
test
***** Result end
...
```

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_patch_string_g.py)
is the generated unit test code.

# Input alias
To make inputs easier, you can define aliases.

In the example [create real instances in a list](#create-multiple-real-instances-in-a-list), instead of 
typing the fully qualified class name, you can create an alias for the class name by adding the following
to the setup function.

>define_alias(alias="ps", full_str="tsdemo.person.Person")

Here is a test run which produces the same result as the example referenced above.

```text
Please provide the value for the parameter (person_list) of type: (typing.List[tsdemo.person.Person]) []: [ps("a", 2), ps("b", 3)]
Expanded alias: ps 2 times.
Result after the expansion: [tsdemo.person.Person("a", 2), tsdemo.person.Person("b", 3)]
Calling get_average_age(person_list=[tsdemo.person.Person("a", 2), tsdemo.person.Person("b", 3)])
```

# Wrapper function
To test a magic string method [here](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/string_method.py),
a wrapper function is used.

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_string_method_g.py)
is the generated test code.

# Annotate a class instance member variable with type information
Proper type information makes input easier in some cases.

In [this class](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/annotate_field_type.py)
the model field is annotated with type information. For comparison, the owner field is not.

As the result, the model field input doesn't need to be quoted. The owner field input does.

Here is an example test run:

```text
...
Please provide the value for the parameter (car) of type: (tsdemo.annotate_field_type.Car) []: m
Created a mock: Mock: name (m_car) spec (<class 'tsdemo.annotate_field_type.Car'>)
Calling get_car_info(car=Mock: name (m_car) spec (<class 'tsdemo.annotate_field_type.Car'>))
Mock object m_car's ( model ) attribute is accessed for the first time.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/annotate_field_type.py", line 15, in get_car_info
    return f"Car model: {car.model}, owner: {car.owner}"

Please provide the value for the model attribute of type: (str) []: camery
Mock attribute value: 'camery'
Mock object m_car's ( owner ) attribute is accessed for the first time.
Call stack:
  File "/home/ray/code/testscribe-demo/tsdemo/annotate_field_type.py", line 15, in get_car_info
    return f"Car model: {car.model}, owner: {car.owner}"

Please provide the value for the owner attribute of type: (any) []: "Bob"
Mock attribute value: 'Bob'
***** Result:
type: <class 'str'>
value:
Car model: camery, owner: Bob
***** Result end
...
```

# Results that contain class instances

## The class doesn't implement a custom \_\_repr\_\_ method.
The result display and generated assertions will be based on member fields.

The target function [create_simple_class_instance](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/object_result.py)
returns an instance of the class SimpleClass, 
which doesn't define a custom \_\_repr\_\_ method.

Here is an example test run:

```text
...
***** Result:
type: tsdemo.object_result.SimpleClass
value:
Object(type (tsdemo.object_result.SimpleClass), members ({'str_field': 'a', 'int_field': 1}))
***** Result end
...
```
[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_object_result_g.py)
is the generated test code.

## The class implements a custom \_\_repr\_\_ method.
The result display and generated assertions will be based on the result of repr(object).

The target function 
[create_class_with_repr_instance](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/object_with_repr_result.py)
returns an instance of the class ClassWithRepr, which defines a custom \_\_repr\_\_ method.

Here is an example test run:

```text
...
***** Result:
type: tsdemo.object_with_repr_result.ClassWithRepr
value:
Object(type (tsdemo.object_with_repr_result.ClassWithRepr), repr (ClassWithRepr(str_field='a', int_field=1)))
***** Result end
...
```
[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_object_with_repr_result_g.py)
is the generated test code.