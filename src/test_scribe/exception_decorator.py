from __future__ import annotations

import functools
import traceback

from click import Abort

from test_scribe.execution_util import ERROR_RETURN_CODE
from test_scribe.log import log


def get_exception_detail_string(e):
    return "".join(traceback.format_exception(type(e), e, e.__traceback__))


def log_exception(e: BaseException):
    exception_msg = get_exception_detail_string(e)
    msg = f"Aborted due to an exception:\n{exception_msg}"
    log(msg)
    raise Abort(ERROR_RETURN_CODE)


def exception_handler(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            return log_exception(e)

    return wrapper_decorator
