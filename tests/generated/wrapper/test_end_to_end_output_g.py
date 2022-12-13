from wrapper.end_to_end_output import function_call_output, method_call_output, mock_property_output, retry_invalid_input_output


def test_function_call_output():
    result = function_call_output()
    assert result == """\
Source file to test: tests/test_data/service_call.py
Function to test: gen_name
Target module to test: test_data.service_call
Output root directory cmd line option: 
Output root directory: 
The target function: gen_name has the signature: (service: 'Service', keyword: 'str', start_number: 'int')
There is no existing test scribe file at /test_data/service_call.tscribe
Calling the setup function setup.setup.
setup function is called.
Prepare to call the target function.
Getting parameters for the function (gen_name)
Please provide the value for the parameter (service) of type: (test_data.service.Service) []: m
Created a mock: Mock: name (m_service) spec (<class 'test_data.service.Service'>)
Please provide the value for the parameter (keyword) of type: (str) []: a
Please provide the value for the parameter (start_number) of type: (int) []: 1
Calling gen_name(service=Mock: name (m_service) spec (<class 'test_data.service.Service'>), keyword='a', start_number=1)
m_service's search_a_name method is called
with: keyword='key: a'.
Call stack:
  File "tests/test_data/service_call.py", line 9, in gen_name
    name = service.search_a_name("key: " + keyword)

Please provide the value for the return value of type: (str) []: b
Mock call return value: 'b'
m_service's search_a_number method is called
with: seed_number=1.
Call stack:
  File "tests/test_data/service_call.py", line 10, in gen_name
    num = service.search_a_number(start_number)

Please provide the value for the return value of type: (int) []: 2
Mock call return value: 2
m_service's search_a_number method is called
with: seed_number=2.
Call stack:
  File "tests/test_data/service_call.py", line 11, in gen_name
    num2 = service.search_a_number(start_number + 1)

Please provide the value for the return value of type: (int) []: 3
Mock call return value: 3
***** Result:
type: <class 'str'>
value:
{"name": "b", "number": 5}
***** Result end
Test name help: 'test_' prefix will be added automatically. Use a leading '_' to include the target function name as part of the prefix.
Test name: [_]: simple gen
Provide a description of the test. []: integration test
Wrote the generated scribe file to: /test_data/service_call.tscribe
Wrote the generated test file to: /test_data/test_service_call_g.py
"""


def test_method_call_output():
    result = method_call_output()
    assert result == """\
Source file to test: tests/test_data/service.py
Function to test: search_a_name
Target module to test: test_data.service
Output root directory cmd line option: 
Output root directory: 
The target function: search_a_name has the signature: (self, keyword: str) -> str
The target class is: <class 'test_data.service.Service'>
There is no existing test scribe file at /test_data/service.tscribe
Calling the setup function setup.setup.
setup function is called.
Prepare to create an instance of the class: Service
Getting parameters for the function (Service)
Please provide the value for the parameter (prefix) of type: (str) []: a
Calling Service(prefix='a')
Prepare to call the target function.
Getting parameters for the function (Service.search_a_name)
Please provide the value for the parameter (keyword) of type: (str) []: b
Calling Service.search_a_name(keyword='b')
***** Result:
type: <class 'str'>
value:
b: a Alice
***** Result end
Test name help: 'test_' prefix will be added automatically. Use a leading '_' to include the target function name as part of the prefix.
Test name: [_]: 
Provide a description of the test. []: 
Wrote the generated scribe file to: /test_data/service.tscribe
Wrote the generated test file to: /test_data/test_service_g.py
"""


def test_mock_property_output():
    result = mock_property_output()
    assert result == """\
Source file to test: tests/test_data/property_access.py
Function to test: get_car_year
Target module to test: test_data.property_access
Output root directory cmd line option: 
Output root directory: 
The target function: get_car_year has the signature: (c: test_data.car.Car) -> int
There is no existing test scribe file at /test_data/property_access.tscribe
Calling the setup function setup.setup.
setup function is called.
Prepare to call the target function.
Getting parameters for the function (get_car_year)
Please provide the value for the parameter (c) of type: (test_data.car.Car) []: m
Created a mock: Mock: name (m_car) spec (<class 'test_data.car.Car'>)
Calling get_car_year(c=Mock: name (m_car) spec (<class 'test_data.car.Car'>))
Mock object m_car's ( year ) attribute is accessed for the first time.
Call stack:
  File "tests/test_data/property_access.py", line 21, in get_car_year
    return c.year

Please provide the value for the year attribute of type: (int) []: 1
Mock attribute value: 1
***** Result:
type: <class 'int'>
value:
1
***** Result end
Test name help: 'test_' prefix will be added automatically. Use a leading '_' to include the target function name as part of the prefix.
Test name: [_]: 
Provide a description of the test. []: 
Wrote the generated scribe file to: /test_data/property_access.tscribe
Wrote the generated test file to: /test_data/test_property_access_g.py
"""


def test_retry_invalid_input_output():
    result = retry_invalid_input_output()
    assert result == """\
Source file to test: tests/test_data/echo.py
Function to test: echo
Target module to test: test_data.echo
Output root directory cmd line option: 
Output root directory: 
The target function: echo has the signature: (v: Any)
There is no existing test scribe file at /test_data/echo.tscribe
Calling the setup function setup.setup.
setup function is called.
Prepare to call the target function.
Getting parameters for the function (echo)
Please provide the value for the parameter (v) of type: (any) []: a
The value is invalid. Please try again.
Error detail:
name 'a' is not defined
Note: string values may need to be quoted.
Use fully qualified type names where a type is expected.
See the input support section of the user guide for more details.
Please provide the value for the parameter (v) of type: (any) []: test_data.simple.C(1)
Calling echo(v=test_data.simple.C(1))
***** Result:
type: test_data.simple.C
value:
Object(type (test_data.simple.C), members ({'a': 1}))
***** Result end
Test name help: 'test_' prefix will be added automatically. Use a leading '_' to include the target function name as part of the prefix.
Test name: [_]: 
Provide a description of the test. []: 
Wrote the generated scribe file to: /test_data/echo.tscribe
Wrote the generated test file to: /test_data/test_echo_g.py
"""
