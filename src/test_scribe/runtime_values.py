from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from test_scribe.namedvalues import NamedValues


@dataclass(frozen=True)
class RuntimeValues:
    # parameters to the constructor if the target is a method
    init_values: NamedValues
    instance: Any  # class instance
    # The init_values and values have been transformed to a format suitable to be
    # saved in a YAML format.
    values: Optional[NamedValues]
    # The transformed result
    # The result is None if there is an exception.
    result: Any
    exception: Exception
