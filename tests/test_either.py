from pyeffects.Either import *
from pyeffects.Monad import identity
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

    def test_left_either_flat_maps_is_left(self):
        assert Left(random_int()).flat_map(lambda v: Right(v)).is_left()
