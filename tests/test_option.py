from pyeffects.option import *


class TestOption:
    def test_option_of_none_is_empty(self):
        empty_option = Option.of(None)
        assert empty_option.is_empty() and empty_option is empty
