from dataclasses import dataclass


@dataclass
class Context:
    # todo: add stack trace.
    description: str
