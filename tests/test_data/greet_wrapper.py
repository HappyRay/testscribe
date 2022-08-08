from test_data.greet import Greeter


def greet_real_greeter(name: str, to: str, words: str):
    """
    Demonstrate how to test calling multiple methods in the same test.
    :param name:
    :param to:
    :param words:
    :return:
    """
    g = Greeter(name)
    conversation = f"{g.greet(to)}\n{g.say(words)}"
    return conversation


def greet_mock_greeter(g: Greeter, to: str, words: str):
    """
    Demonstrate how to use a mock object as the target instance.

    :param g:
    :param to:
    :param words:
    :return:
    """
    conversation = f"{g.greet(to)}\n{g.say(words)}"
    return conversation
