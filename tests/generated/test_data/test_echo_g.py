from test_data.echo import echo


def test_simple_string():
    """
    A simple string result should use the default flow style in the tscribe yaml file
    """
    result = echo(v='a')
    assert result == 'a'


def test_multiline_string():
    """
    multiline string values should be encoded as block style in the tscribe file.
    """
    result = echo(v='a\nb')
    assert result == """\
a
b"""
