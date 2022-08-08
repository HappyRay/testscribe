class Error(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InputError(Error):
    pass


class UnsupportedDataError(Error):
    pass
