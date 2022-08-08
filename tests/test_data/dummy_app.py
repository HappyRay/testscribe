from typer import Typer
from test_scribe.exception_decorator import exception_handler

app = Typer(name="dummy")


@app.command()
@exception_handler
def raise_exception():
    raise Exception("Test exception")


if __name__ == "__main__":
    app()
