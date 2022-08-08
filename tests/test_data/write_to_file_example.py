from pathlib import Path


def write_to_file_example(content: str, file_path: Path) -> None:
    with open(file_path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    write_to_file_example("hello", Path("write_to_file_test.txt"))
