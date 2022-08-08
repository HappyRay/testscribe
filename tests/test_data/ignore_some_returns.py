class S:
    def do(self, i: int) -> int:
        return i


def ignore_some_returns(s: S):
    s.do(1)
    return s.do(2)
