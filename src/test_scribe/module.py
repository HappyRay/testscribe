from __future__ import annotations

from typing import Collection, List


class Module:
    def __init__(self, module_names: Collection[str]):
        """

        :param module_names:a list of string representing the full module name.
        Parent module name comes first.
        """
        self.names = tuple(module_names)

    def get_package_name_list(self) -> List[str]:
        return list(self.names[:-1])

    def get_module_name_only(self) -> str:
        return self.names[-1]

    def get_module_str(self):
        return ".".join(self.names)


def get_module_from_str(name: str) -> Module:
    return Module(name.split("."))
