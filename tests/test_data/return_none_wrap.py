from test_data.return_none import f, return_none
from test_scribe.mocking_support import patch


def f_wrap():
    patch("test_scribe.return_none.return_none", return_none)
    f()
