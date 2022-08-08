g_aliases = {}


def define_alias(alias: str, full_str: str):
    g_aliases[alias] = full_str
    # return the dictionary to make testing easier
    return g_aliases
