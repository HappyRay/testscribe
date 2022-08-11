# explict import from builtins to allow mocking of builtins.
from builtins import open


def write_to_file(content: str, file_name: str):
    with open(file_name, "w") as f:
        f.write(content)
