from testscribe import global_var


def log(s: str) -> None:
    global_var.g_io.log(s)
