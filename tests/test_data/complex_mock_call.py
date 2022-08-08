from pathlib import Path


class Service:
    def f(self, p: Path) -> None:
        pass


def call_mock_service_with_object(s: Service):
    s.f(Path("foo"))
