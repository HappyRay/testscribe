from testscribe.value_input_cli import post_process_raw_input
from testscribe.value_util import InputValue


def post_process_raw_input_wrapper_special_value():
    r = post_process_raw_input(raw_input_str="ignore", t=int)
    # InputValue has special handing. So translate it to a regular tuple here.
    assert isinstance(r, InputValue)
    return r.expression, r.value
