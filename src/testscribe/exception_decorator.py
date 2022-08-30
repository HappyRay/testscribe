#  Copyright 2022 Ruiguo (Ray) Yang
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

from __future__ import annotations

import functools
import traceback

from click import Abort

from testscribe.execution_util import ERROR_RETURN_CODE
from testscribe.log import log


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
