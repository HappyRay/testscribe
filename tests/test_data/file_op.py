def write_to_file(content: str, file_name: str):
    with open(file_name, "w") as f:
        f.write(content)
