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

# <a name="create-class-instance-in-list"></a>Create multiple class instances in a list
The function [get_average_age](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/objects_in_list.py) takes a
list of [Person](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/person.py) object as a parameter.

An example test run output:

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

[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tests/generated/tsdemo/test_objects_in_list_g.py)
is the generated unit test code.