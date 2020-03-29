from pyeffects.Option import *
from pyeffects.Monad import identity
from pyeffects.Try import Try
from .random_int_generator import random_int


class TestOption:
    @staticmethod
    def _sq_int(v):
        return Option.of(v * v)

    @staticmethod
    def _dbl_int(v):
        return Option.of(v + v)

    def test_option_of_none_is_empty(self):
        empty_option = Option.of(None)
        assert empty_option.is_empty() and empty_option is empty

    def test_option_right_identity(self):
        value = random_int()
        assert Option.of(value).flat_map(identity) == value

    def test_option_left_identity(self):
        value = random_int()
        assert Option.of(value).flat_map(self._sq_int).get() == self._sq_int(value).get()

    def test_option_associativity(self):
        value = random_int()
        value1 = Option.of(value).flat_map(lambda v1: self._sq_int(v1).flat_map(lambda v2: self._dbl_int(v2)))
        value2 = Option.of(value).flat_map(self._sq_int).flat_map(self._dbl_int)
        assert value1.get() == value2.get()

    def test_empty_option_flat_maps_to_empty(self):
        assert empty.flat_map(lambda v: Option.of(v)).is_empty()

    def test_option_flat_map_requires_callable(self):
        result = Try.of(lambda: Some(random_int()).flat_map(random_int()))
        assert result.is_failure() and isinstance(result.error(), TypeError)

    def test_option_repr(self):
        assert str(Some(random_int())).startswith("Some")
        assert str(empty).startswith("Empty")
