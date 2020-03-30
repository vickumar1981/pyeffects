from pyeffects.Either import *
from pyeffects.Monad import identity
from pyeffects.Try import Try
from .random_int_generator import random_int


class TestEither:
    @staticmethod
    def _sq_int(v):
        return Right(v * v)

    @staticmethod
    def _dbl_int(v):
        return Right(v + v)

    def test_either_is_right_by_default(self):
        assert Either.of(random_int()).is_right()

    def test_left_either_properties(self):
        value = Left(random_int())
        assert value.is_left() and not value.is_right()

    def test_right_either_properties(self):
        value = Right(random_int())
        assert value.is_right() and not value.is_left()

    def test_either_right_identity(self):
        value = random_int()
        assert Right(value).flat_map(identity) == value

    def test_either_left_identity(self):
        value = random_int()
        assert Right(value).flat_map(self._sq_int).get() == self._sq_int(value).get()

    def test_either_associativity(self):
        value = random_int()
        value1 = Right(value).flat_map(lambda v1: self._sq_int(v1).flat_map(lambda v2: self._dbl_int(v2)))
        value2 = Right(value).flat_map(self._sq_int).flat_map(self._dbl_int)
        assert value1.get() == value2.get()

    def test_right_value_equals_get(self):
        value = random_int()
        assert Right(value).right() == Right(value).get()

    def test_left_either_flat_maps_is_left(self):
        value = random_int()
        result = Left(value).flat_map(lambda v: Right(v))
        assert result.is_left() and result.left() == value

    def test_left_maps_does_not_map(self):
        value = random_int()
        assert Left(value).map(lambda v: v * 2).left() == value

    def test_left_map_requires_callable(self):
        result = Try.of(lambda: Left(random_int()).map(random_int()))
        assert result.is_failure() and isinstance(result.error(), TypeError)

    def test_either_flat_map_requires_callable(self):
        result = Try.of(lambda: Right(random_int()).flat_map(random_int()))
        assert result.is_failure() and isinstance(result.error(), TypeError)

    def test_either_repr(self):
        assert str(Right(random_int())).startswith("Right")
        assert str(Left(random_int())).startswith("Left")
