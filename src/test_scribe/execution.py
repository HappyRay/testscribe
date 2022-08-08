import logging.config
import traceback
from dataclasses import dataclass
from inspect import signature
from pathlib import Path
from typing import Optional, Callable, List, Any, Dict

from test_scribe import global_var
from test_scribe.context import Context
from test_scribe.error import UnsupportedDataError
from test_scribe.execution_util import (
    infer_unit_test_file_path_from_scribe_file,
    call_target_function,
)
from test_scribe.generate_tests import generate_unit_test_file
from test_scribe.input_params import (
    InputParams,
    get_target_function_name,
    get_target_class_name,
    get_scribe_file_path,
)
from test_scribe.log import log
from test_scribe.model import generate_model
from test_scribe.model_type import TestModel, AllTests, get_type_str
from test_scribe.namedvalues import NamedValues
from test_scribe.parameter_value_input import get_parameter_value
from test_scribe.patcher import Patcher
from test_scribe.reflection_util import get_full_spec_name
from test_scribe.runtime_values import RuntimeValues
from test_scribe.save_scribe_file import generate_scribe_file
from test_scribe.transformer import transform_value
from test_scribe.value_util import get_value

logger = logging.getLogger(__name__)


@dataclass
class CallResult:
    arguments: Optional[NamedValues]
    result: Any
    exception: Optional[Exception]


def transform_named_values(named_values: NamedValues) -> NamedValues:
    return NamedValues(transform_value(named_values.as_list()))


def get_args_and_call(func: Callable, default: NamedValues) -> CallResult:
    """
    Gather arguments for the given function and call it.

    :param func:
    :param default: the default for the arguments
    :return:
    """
    name = func.__qualname__
    log(f"Getting parameters for the function ({name})")
    description = f"Parameters for the function ({name})"
    named_values = get_parameter_value(
        func=func, context=Context(description=description), default=default
    )
    # Have to make a copy before invoking the function
    transformed_named_values = transform_named_values(named_values)
    values = [get_value(value) for _, value in named_values.as_list()]
    sig = signature(func)
    args = sig.bind(*values)
    arg_str = named_values.as_arg_str()
    log(f"Calling {name}({arg_str})")
    exception = None
    try:
        ret_value = call_target_function(func, args)
    except Exception as e:
        log(f"The function {func.__qualname__} throws an exception.")
        # todo: filter out the system frames at the bottom of the stack.
        log(traceback.format_exc())
        ret_value = None
        exception = e
    return CallResult(
        arguments=transformed_named_values, result=ret_value, exception=exception
    )


def get_default_init_parameters(
    test_to_infer_default_inputs: Optional[TestModel],
) -> NamedValues:
    if test_to_infer_default_inputs:
        return test_to_infer_default_inputs.init_parameters
    else:
        return NamedValues()


def create_instance(
    clazz: type, test_to_infer_default_inputs: Optional[TestModel]
) -> CallResult:
    """
    Create an instance of the class being tested.
    :param test_to_infer_default_inputs:
    :param clazz:
    :return:
    """
    name = clazz.__qualname__
    log(f"Prepare to create an instance of the class: {name}")
    default = get_default_init_parameters(test_to_infer_default_inputs)
    return get_args_and_call(func=clazz, default=default)


def get_test_to_infer_default_inputs(
    tests: List[TestModel],
    index_of_test_to_update: int,
    function_name: str,
    class_name: str,
) -> Optional[TestModel]:
    if index_of_test_to_update >= 0:
        logger.info(
            f"Use the test being updated to retrive default values."
            f" index: {index_of_test_to_update}, name: {tests[index_of_test_to_update].name}"
        )
        return tests[index_of_test_to_update]
    # use the newest test with the same target function to infer default inputs
    # Note that this assumes newer tests appear in this list earlier.
    for t in tests:
        if t.target_func_name == function_name and t.target_class_name == class_name:
            logger.info(
                f"Use a test with the same target to retrive default. name: {t.name}"
            )
            return t
    logger.info("Can't find a test with the same target to retrive defaults values.")
    return None


def execute_and_generate(
    input_params: InputParams,
    all_tests: AllTests,
    index_of_test_to_update: int,
):
    runtime_values = create_instance_and_run(
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
        input_params=input_params,
    )
    generate_test(
        input_params=input_params,
        runtime_values=runtime_values,
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
    )


def create_instance_and_run(
    all_tests: AllTests, index_of_test_to_update: int, input_params: InputParams
) -> RuntimeValues:
    test_to_infer_default_inputs = get_test_to_infer_default_inputs(
        tests=all_tests.tests,
        index_of_test_to_update=index_of_test_to_update,
        function_name=get_target_function_name(input_params),
        class_name=get_target_class_name(input_params),
    )
    global_var.g_test_to_infer_default_inputs = test_to_infer_default_inputs
    try:
        function_instance = get_function_instance(
            input_params=input_params,
            test_to_infer_default_inputs=test_to_infer_default_inputs,
        )
        call_result = run_target_function(
            exception=function_instance.exception,
            func=function_instance.func,
            test_to_infer_default_inputs=test_to_infer_default_inputs,
        )
    finally:
        stop_patches(global_var.g_patchers)

    return RuntimeValues(
        init_values=function_instance.init_values,
        instance=function_instance.target_instance,
        values=call_result.arguments,
        result=transform_and_show_result(call_result),
        exception=call_result.exception,
    )


def transform_and_show_result(call_result: CallResult) -> Any:
    if call_result.exception:
        return None
    raw_result = call_result.result
    try:
        transformed_result = transform_value(raw_result)
    except UnsupportedDataError as e:
        log(f"Result:\n{raw_result}")
        raise e
    # show the transformed result to have better display of certain types
    # e.g. showing the members of an object.
    show_result(transformed_result)
    return transformed_result


def show_result(result: Any) -> str:
    result_str = f"***** Result:\n{show_result_internal(result)}\n***** Result end"
    log(result_str)
    return result_str


def show_result_internal(result: Any) -> str:
    # todo: force the str method when a complex object
    # such as ObjectModel object is used inside a container
    # to have a better display.
    return f"type: {get_type_str(result)}\nvalue:\n{result}"


def stop_patches(patchers: Dict[str, Patcher]) -> None:
    for p in patchers.values():
        p.instance.stop()


def run_target_function(
    exception: Optional[Exception],
    func: Callable,
    test_to_infer_default_inputs: Optional[TestModel],
) -> CallResult:
    if exception:
        return CallResult(arguments=None, result=None, exception=exception)
    else:
        log("Prepare to call the target function.")
        default = (
            test_to_infer_default_inputs.parameters
            if test_to_infer_default_inputs
            else NamedValues()
        )
        logger.debug(f"run target function. Default parameters: {default}")
        return get_args_and_call(func=func, default=default)


@dataclass
class FunctionInstance:
    func: Callable
    # Exception thrown when creating a class instance if the func is a method
    exception: Optional[Exception]
    # If the func is a method, the bounded class instance. Otherwise None
    target_instance: Any
    # If the func is a method, the arguments to the bounded class' constructor
    init_values: NamedValues


def get_function_instance(
    input_params: InputParams, test_to_infer_default_inputs: TestModel
) -> FunctionInstance:
    exception = None
    clazz = input_params.clazz
    func = input_params.func
    if clazz:
        # todo: handle class methods. They don't need to create a class
        #  instance.
        call_result = create_instance(clazz, test_to_infer_default_inputs)
        target_instance = call_result.result
        init_values = call_result.arguments
        exception = call_result.exception
        if not exception:
            function_name = get_target_function_name(input_params)
            func = getattr(target_instance, function_name)
    else:
        target_instance = None
        init_values = NamedValues()
    return FunctionInstance(
        func=func,
        init_values=init_values,
        target_instance=target_instance,
        exception=exception,
    )


def generate_test(
    input_params: InputParams,
    runtime_values: RuntimeValues,
    all_tests: AllTests,
    index_of_test_to_update: int,
):
    new_all_tests = generate_model(
        input_params=input_params,
        runtime_values=runtime_values,
        all_tests=all_tests,
        index_of_test_to_update=index_of_test_to_update,
    )
    scribe_file_path = get_scribe_file_path(
        output_root_dir=input_params.output_root_dir, module=input_params.module
    )
    save_file(scribe_file_path=scribe_file_path, all_tests=new_all_tests)
    end(scribe_file_path=scribe_file_path)


def end(scribe_file_path: Path):
    global_var.g_io.end(scribe_file_path)


def save_file(scribe_file_path: Path, all_tests: AllTests):
    generate_scribe_file(scribe_file_path=scribe_file_path, all_tests=all_tests)
    test_file_path = infer_unit_test_file_path_from_scribe_file(scribe_file_path)
    generate_unit_test_file(test_file_path=test_file_path, all_tests=all_tests)


def run_setup_func(f: Optional[Callable]):
    if f is not None:
        log(f"Calling the setup function {get_full_spec_name(f)}.")
        f()
