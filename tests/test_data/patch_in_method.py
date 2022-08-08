import test_data.simple


class MethodPatched:
    def __init__(self, i: int):
        self.v = i

    def foo(self) -> int:
        return self.v + test_data.simple.INT_VALUE
