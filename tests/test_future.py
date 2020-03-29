from pyeffects.Future import *
from pyeffects.Try import Try
from .random_int_generator import random_int


class TestOption:
    @staticmethod
    def _sq_int(v):
        return Future.of(v * v)

    @staticmethod
    def _dbl_int(v):
        return Future.of(v + v)

    def _fail_future(self):
        raise RuntimeError("Failed")

    def test_future_success_properties(self):
        value = random_int()
        assert Future.of(value).get().get() == value

    def test_future_right_identity(self):
        value = random_int()
        assert Future.of(value).flat_map(lambda v: Future.of(v)).get().get() == value

    def test_future_left_identity(self):
        value = random_int()
        assert Future.of(value).flat_map(self._sq_int).get().get() == self._sq_int(value).get().get()

    def test_future_associativity(self):
        value = random_int()
        value1 = Future.of(value).flat_map(lambda v1: self._sq_int(v1).flat_map(lambda v2: self._dbl_int(v2)))
        value2 = Future.of(value).flat_map(self._sq_int).flat_map(self._dbl_int)
        assert value1.get().get() == value2.get().get()

    def test_failed_future_flat_maps_to_failure(self):
        assert Future.run(self._fail_future).flat_map(lambda v: Future.of(v)).get().is_failure()

    def test_future_flat_map_requires_callable(self):
        result = Try.of(lambda: Future.of(random_int()).flat_map(random_int()))
        assert result.is_failure() and isinstance(result.error(), TypeError)

    def test_future_repr(self):
        assert str(Future.of(random_int())).startswith("Future")
