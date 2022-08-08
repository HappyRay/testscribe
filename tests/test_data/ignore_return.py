class S:
    def do(self) -> int:
        return 1


def ignore_return(s: S):
    s.do()
