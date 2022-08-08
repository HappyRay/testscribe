from test_scribe.user_triggered_exception import UserTriggeredException


def get_user_triggered_exception_repr(e: BaseException):
    return repr(UserTriggeredException(e))
