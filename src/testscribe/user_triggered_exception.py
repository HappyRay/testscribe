from __future__ import annotations

from dataclasses import dataclass

from testscribe.base_reflection_util import get_class_instance_repr_with_full_name


@dataclass
class UserTriggeredException:
    """
    Used in an input expression to cause a mock call to throw the
    given exception.
    """

    exception: BaseException

    def __repr__(self):
        """
        Custom repr to allow easier code generation
        :return:
        """
        return get_class_instance_repr_with_full_name(self.exception)
