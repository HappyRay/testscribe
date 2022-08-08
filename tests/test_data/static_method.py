class StaticService:
    @staticmethod
    def do() -> int:
        return 1


def call_static_method(s: StaticService):
    return s.do()
