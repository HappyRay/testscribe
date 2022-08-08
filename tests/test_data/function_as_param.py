from __future__ import annotations

import json
from typing import Callable


def calculate(initial: int) -> int:
    # Can be some complex computation.
    return initial * 2


def calc(seed: int, f: Callable[[int], int]) -> str:
    """
    An example of a function as a parameter.

    :param seed:
    :param f:
    :return:
    """
    result = f(seed + 1)
    d = {"result": result + 1}
    json_str = json.dumps(d)
    return json_str


def calc2(seed: int) -> str:
    """
    Compare to the calc function, it calls the predefined function calculate function.
    If this function is tested directly, it will call the real calculate function.

    To mock out the calculate function, a wrapper test function needs to be written.

    :param seed:
    :return:
    """
    return calc(seed=seed, f=calculate)


if __name__ == "__main__":
    r = calc(1, calculate)
    print(r)
