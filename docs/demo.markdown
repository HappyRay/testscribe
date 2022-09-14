---
layout: my-home
title: demo
---
# Mock a class instance passed as a parameter
The function search_name takes a service object as a parameter.
The service may involve a database or a network call.
It's easier to test by mocking it.
[Here](https://github.com/HappyRay/testscribe-demo/blob/main/tsdemo/simple_mock.py) is the function definition.

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