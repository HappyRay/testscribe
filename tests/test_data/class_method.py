class ClassService:
    i = 1

    @classmethod
    def do(cls) -> int:
        return cls.i


def call_class_method(s: ClassService):
    return s.do()
