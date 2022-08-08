class Greeter:
    def __init__(self, my_name: str):
        self.my_name = my_name

    def greet(self, to: str) -> str:
        return f"Hello {to}. My name is {self.my_name}"

    def say(self, words: str) -> str:
        return f"{self.my_name} says {words}"

    def say_with_cap(self, capitalize: bool, words: str) -> str:
        say_words = words.capitalize() if capitalize else words
        return self.say(say_words)
