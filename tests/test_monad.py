from pyeffects.Option import *
from pyeffects.Try import *
from .random_int_generator import random_int


class TestMonad:
    def test_monad_pure_not_implemented(self):
        err = Try.of(lambda: Monad.of(random_int()))
        assert err.is_failure() and isinstance(err.error(), NotImplementedError)

    def test_monad_map(self):
        value = Some(random_int())
        assert value.map(lambda v: v + v).get() == value.get() * 2

    def test_get_on_empty_monad_throws_type_error(self):
        err = Try.of(lambda: empty.get())
        assert err.is_failure() and isinstance(err.error(), TypeError)

    def test_monad_get_or_else_with_success(self):
        value = random_int()
        assert Some(value).get_or_else(random_int()) == value

    def test_monad_get_or_else_with_failure(self):
        value = random_int()
        assert empty.get_or_else(value) == value

    def test_monad_or_else_supply_with_success(self):
        value = random_int()
        assert Some(value).or_else_supply(lambda: random_int()) == value

    def test_monad_or_else_suplly_with_failure(self):
        value = random_int()
        assert empty.or_else_supply(lambda: value) == value

    def test_monad_or_else_with_success(self):
        value = random_int()
        result = Some(value).or_else(Some(random_int()))
        assert result.get() == value

    def test_monad_or_else_with_failure(self):
        value = random_int()
        result = empty.or_else(Some(value))
        assert result.get() == value
