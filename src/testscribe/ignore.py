from __future__ import annotations


class IgnoreReturnValue:
    def __repr__(self):
        # Use the string as the return value of a mock call.
        # It has to be a valid expression since it will be used in the generated test.
        return "'Ignored'"


# Use this variable when the special input expression "ignore" is used for a mock
# return value to ignore the return value.
# It's useful if the return value is not used in the production code.
IGNORED = IgnoreReturnValue()
