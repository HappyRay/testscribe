from unittest.mock import patch, create_autospec

from test_scribe.model_type import MockNameModel, TestModel, MockModel
from test_scribe.value_input_util import transform_real_default_value


def transform_real_default_value_wrapper():
    m_test_model = create_autospec(spec=TestModel)
    m_mock_model = create_autospec(spec=MockModel)
    m_test_model.mocks = [m_mock_model]
    m_mock_model.name = "a"
    m_mock_model.spec_str = "spec"

    # During the test run global_var.g_test_to_infer_default_inputs is set
    # after the setup function is called so using the setup function to patch
    # doesn't work.
    with patch(
        "test_scribe.value_input_util.global_var.g_test_to_infer_default_inputs",
        m_test_model,
    ):
        return transform_real_default_value(MockNameModel("a"))
