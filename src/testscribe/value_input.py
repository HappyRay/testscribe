from __future__ import annotations

import logging
from typing import Any

from testscribe import global_var
from testscribe.context import Context

logger = logging.getLogger(__name__)


def get_one_value(
    prompt_name: str, t: type, context: Context, default: Any, name: str = ""
) -> Any:
    """

    :param prompt_name: the string used as a prompt for the input
    :param t:
    :param context:
    :param default:
    :param name: a name associated with the value e.g. a parameter's name
    :return:
    """
    logger.debug(
        f"Get one value. prompt_name: {prompt_name}, name: {name}, "
        f"type: {t}, context: {context}, default: {default} "
    )
    # signature returns None, get_type_hints returns <class 'NoneType'>
    if t in [None, type(None)]:
        return None
    return global_var.g_io.get_one_value(
        prompt_name=prompt_name, name=name, t=t, default=default, context=context
    )
