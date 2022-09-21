---
layout: my-home
title: demo
---
# <a name="mock-class-instance"></a>Mock a class instance
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

# <a name="create-class-instance"></a>Create a class instance
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

# <a name="objects-in-list"></a>multiple class instances in a list
The function [get_average_age](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/objects_in_list.py) takes a
list of [Person](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/person.py) object as a parameter.

An example test run with real instances:

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

An example test run with mocked instances:
```text
Please provide the value for the parameter (person_list) of type: (typing.List[tsdemo.person.Person]) [[tsdemo.person.Person("a", 2), tsdemo.person.Person("b", 3)]]: [m, m]
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

# <a name="raise-exception"></a>Raise an exception in a mock call
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
