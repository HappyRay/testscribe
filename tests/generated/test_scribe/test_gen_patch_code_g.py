import test_scribe.model_type
from test_scribe.api.mock_api import get_normalized_mock_calls
from unittest.mock import ANY, call, create_autospec
from test_scribe.gen_patch_code import generate_patch_str


def test_generate_patch_statement_dict_as_replacement():
    input_mock: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    input_mock.target = 't'
    input_mock.replacement = {'a': 1}
    result = generate_patch_str(patches=[input_mock])
    assert result == """\

    with patch('t', {'a': 1}):"""
    input_mock.assert_not_called()


def test_generate_patch_statement_mock_as_replacement():
    input_mock: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    input_mock.target = 't'
    input_mock.replacement = test_scribe.model_type.MockNameModel("m")
    result = generate_patch_str(patches=[input_mock])
    assert result == """\

    with patch('t', m):"""
    input_mock.assert_not_called()


def test_generate_patch_statement_multiple_patch():
    input_mock: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    input_mock_1: test_scribe.model_type.PatchModel = create_autospec(spec=test_scribe.model_type.PatchModel)
    input_mock.target = 't'
    input_mock.replacement = 1
    input_mock_1.target = 't1'
    input_mock_1.replacement = 2
    result = generate_patch_str(patches=[input_mock, input_mock_1])
    assert result == """\

    with patch('t', 1), patch('t1', 2):"""
    input_mock.assert_not_called()
    input_mock_1.assert_not_called()


def test_generate_patch_statement_no_patch():
    result = generate_patch_str(patches=[])
    assert result == ''
