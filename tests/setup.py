from test_scribe.api.alias import define_alias


def setup():
    print("setup function is called.")
    define_alias(alias="td", full_str="test_data")
    define_alias(alias="ts", full_str="test_scribe")
    # define_alias(alias="mn", full_str="test_scribe.model_type.MockNameModel")
    define_alias(alias="nv", full_str="test_scribe.namedvalues.NamedValues")
    define_alias(alias="optional", full_str="typing.Optional")
    define_alias(alias="union", full_str="typing.Union")
    # define_alias(alias="mp", full_str="test_scribe.mock_proxy.MockProxy")
    # define_alias(alias="pm", full_str="test_scribe.model_type.PatchModel")
    # define_alias(alias="tp", full_str="typing")
    # define_alias(alias="tms", full_str="test_scribe.mocking_support")
    # patch_with_mock(target=func_with_side_effect)
    # patch_with_mock(target=MockProxy)
    # Use the inital state of the g_mock_name_counter variable.
    # patch_with_expression(
    #     target_str="test_scribe.global_var.g_mock_name_counter",
    #     expression="collections.Counter(test_scribe.global_var.g_mock_name_counter)",
    # )
    # patch_globals_modified_by_mock_proxy()
    # patch_g_mock_name_counter()
    # patch_with_mock("test_scribe.sync_cmd.get_all_scribe_files")

    # patch_with_mock(target="test_data.file_op.open", spec=text_open_spec)
    # an altertive way to patch a mock with a different spec
    # patch_with_expression(target_str="test_data.file_op.open", expression="m(test_scribe.api.mock_api.text_open_spec)")
    # patch_with_expression(target_str="test_scribe.eval_expression.g_aliases", expression='{"a": "hello", "b": "World"}')
