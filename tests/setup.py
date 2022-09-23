from testscribe.api.alias import define_alias


def setup():
    print("setup function is called.")
    define_alias(alias="td", full_str="test_data")
    define_alias(alias="ts", full_str="testscribe")
    # define_alias(alias="mn", full_str="testscribe.model_type.MockNameModel")
    define_alias(alias="nv", full_str="testscribe.namedvalues.NamedValues")
    define_alias(alias="optional", full_str="typing.Optional")
    define_alias(alias="union", full_str="typing.Union")
    # define_alias(alias="mp", full_str="testscribe.mock_proxy.MockProxy")
    # define_alias(alias="pm", full_str="testscribe.model_type.PatchModel")
    # define_alias(alias="tp", full_str="typing")
    # define_alias(alias="tms", full_str="testscribe.mocking_support")
    # patch_with_mock(target=func_with_side_effect)
    # patch_with_mock(target=MockProxy)
    # Use the initial state of the g_mock_name_counter variable.
    # patch_with_expression(
    #     target_str="testscribe.global_var.g_mock_name_counter",
    #     expression="collections.Counter(testscribe.global_var.g_mock_name_counter)",
    # )
    # patch_globals_modified_by_mock_proxy()
    # patch_g_mock_name_counter()
    # patch_with_mock("testscribe.sync_cmd.get_all_scribe_files")

    # patch_with_mock(target="test_data.file_op.open", spec=text_open_spec)
    # an alternative way to patch a mock with a different spec
    # patch_with_expression(target_str="test_data.file_op.open", expression="m(testscribe.api.mock_api.text_open_spec)")
    # patch_with_expression(target_str="testscribe.eval_expression.g_aliases", expression='{"a": "hello", "b": "World"}')
