class BadInit:
    def __init__(self):
        raise Exception("bad init")

    def f(self):
        pass
