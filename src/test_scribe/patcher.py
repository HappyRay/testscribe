from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any
from unittest.mock import patch

from test_scribe import global_var
from test_scribe.log import log
from test_scribe.model_type import MockNameModel
from test_scribe.transformer import transform_value
from test_scribe.util import remove_trailing_numbers
from test_scribe.value_util import get_value, get_value_repr


def patch_common(target_str: str, replacement: Any):
    """
    :param target_str:
    :param replacement:
    :return:
    """
    patchers = global_var.g_patchers
    value = get_value(replacement)
    value_str = get_value_repr(value)
    log(f"Patch {target_str} with {value_str}")
    instance = patch(target=target_str, new=value)
    patchers[target_str] = create_patcher(
        target_str=target_str, instance=instance, replacement=replacement
    )
    instance.start()


def create_patcher(target_str: str, instance, replacement: Any) -> Patcher:
    """

    :param target_str: the target symbol to patch
    :param instance: the return value of a mock.patch call. The type _patch is
    an internal type of mock.
    :param replacement:
    :return:
    """
    # Need to take a snapshot of the value
    # so that the generated code will use the initial value not the potentially
    # mutated value. e.g. if the replacement is a list, it can potentially
    # change its value after execution.

    # Transform process is itself a deepcopy.

    # Wrapping the value as an ExpressionModel doesn't work when the value
    # contains a MockProxy
    return Patcher(
        target=target_str,
        instance=instance,
        replacement_spec=transform_value(replacement),
    )


@dataclass
class Patcher:
    target: str
    # the return value of a mock.patch call. The type _patch is
    #     an internal type of mock. It can't be used directly here.
    instance: Any
    # A transformed copy of the origianl replacement value
    replacement_spec: Any


def remove_duplicate_patch(target_str: str):
    patchers = global_var.g_patchers
    if target_str in patchers:
        log(f"Remove previous patch of the same target {target_str}")
        patcher = patchers.pop(target_str)
        patcher.instance.stop()
        remove_mock(patcher.replacement_spec)


def remove_mock(replacement_spec: Any) -> None:
    if isinstance(replacement_spec, MockNameModel):
        name = replacement_spec.name
        assert name in global_var.g_name_mock_dict
        del global_var.g_name_mock_dict[name]
        remove_mock_name(name)


def remove_mock_name(name: str):
    nomalized_name = remove_trailing_numbers(name)
    decrement_counter(
        name_counter=global_var.g_mock_name_counter, nomalized_name=nomalized_name
    )


def decrement_counter(name_counter: Counter, nomalized_name: str) -> Counter:
    assert nomalized_name in name_counter
    name_counter[nomalized_name] -= 1
    if name_counter[nomalized_name] == 0:
        del name_counter[nomalized_name]
    return name_counter
