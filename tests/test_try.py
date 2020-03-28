from pyeffects.Try import *
from pyeffects.Monad import identity
from .random_int_generator import random_int


class TestOption:
    @staticmethod
    def _sq_int(v):
        return Try.of(lambda: v * v)

    @staticmethod
    def _dbl_int(v):
        return Try.of(lambda: v + v)

    def _fail_try(self):
        raise RuntimeError("Failed")

    def test_try_of_exception_is_failure(self):
        failed_try = Try.of(self._fail_try)
        err = failed_try.error()
        assert failed_try.is_failure()
        assert isinstance(err, RuntimeError) and str(err) == "Failed"

    def test_recover_from_failed_try_is_success(self):
        value = random_int()
        failed_try = Try.of(self._fail_try)
        recovered_try = failed_try.recover(RuntimeError, lambda: value)
        assert recovered_try.is_success() and recovered_try.get() == value

    def test_recover_from_failed_try_depends_on_error(self):
        value = random_int()
        failed_try = Try.of(self._fail_try)
        assert failed_try.recover(AssertionError, lambda: value).is_failure()

    def test_try_right_identity(self):
        value = random_int()
        assert Try.of(lambda: value).flat_map(identity) == value

    def test_try_left_identity(self):
        value = random_int()
        assert Try.of(lambda: value).flat_map(self._sq_int).get() == self._sq_int(value).get()

    def test_try_associativity(self):
        value = random_int()
        value1 = Try.of(lambda: value).flat_map(lambda v1: self._sq_int(v1).flat_map(lambda v2: self._dbl_int(v2)))
        value2 = Try.of(lambda: value).flat_map(self._sq_int).flat_map(self._dbl_int)
        assert value1.get() == value2.get()

    def test_try_map_function(self):
        value = random_int()
        assert Try.of(lambda: value).map(lambda v: v + v).get() == value * 2

    def test_failed_try_flat_maps_to_failure(self):
        assert Try.of(self._fail_try).flat_map(self._dbl_int).is_failure()
