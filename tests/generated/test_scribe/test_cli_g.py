import click.termui
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from unittest.mock import patch
from test_scribe.cli import get_test_description_cli


def test_get_test_description_from_user_cli():
    m_prompt: click.termui.prompt = create_autospec(spec=click.termui.prompt)
    m_prompt.return_value = 'a b'
    with patch('test_scribe.cli.prompt', m_prompt):
        result = get_test_description_cli(default='default')
    assert result == 'a b'
    m_prompt_mock_calls = get_normalized_mock_calls(m_prompt, click.termui.prompt)
    assert m_prompt_mock_calls == [
        call(text='Provide a description of the test.', default='default'),
    ]


def test_get_test_description_from_user_cli_empty():
    m_prompt: click.termui.prompt = create_autospec(spec=click.termui.prompt)
    m_prompt.return_value = "''"
    with patch('test_scribe.cli.prompt', m_prompt):
        result = get_test_description_cli(default='default')
    assert result == ''
    m_prompt_mock_calls = get_normalized_mock_calls(m_prompt, click.termui.prompt)
    assert m_prompt_mock_calls == [
        call(text='Provide a description of the test.', default='default'),
    ]
