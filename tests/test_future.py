from pyeffects.Future import *
from pyeffects.Try import Try
from .random_int_generator import random_int
import time


class TestFuture:
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
        assert Future.of(value).get() == value

    def test_future_right_identity(self):
        value = random_int()
        assert Future.of(value).flat_map(lambda v: Future.of(v)).get() == value

    def test_future_left_identity(self):
        value = random_int()
        assert (
            Future.of(value).flat_map(self._sq_int).get() == self._sq_int(value).get()
        )

    def test_future_associativity(self):
        value = random_int()
        value1 = Future.of(value).flat_map(
            lambda v1: self._sq_int(v1).flat_map(lambda v2: self._dbl_int(v2))
        )
        value2 = Future.of(value).flat_map(self._sq_int).flat_map(self._dbl_int)
        assert value1.get() == value2.get()

    def test_future_completes_async_with_value(self):
        value = random_int()

        def delayed_result():
            time.sleep(0.1)
            return value

        result = Future.run(delayed_result)
        assert result.is_done() is False
        assert result.get() is None
        time.sleep(0.2)
        assert result.is_done() is True
        assert result.get() == value

    def test_failed_future_flat_maps_to_failure(self):
        assert (
            Future.run(self._fail_future).flat_map(lambda v: Future.of(v)).is_failure()
        )

    def test_future_flat_map_requires_callable(self):
        result = Try.of(lambda: Future.of(random_int()).flat_map(random_int()))
        assert result.is_failure() and isinstance(result.error(), TypeError)

    def test_future_repr(self):
        assert str(Future.of(random_int())).startswith("Future")

    def test_combining_futures_with_flat_map(self):
        value1 = random_int()
        value2 = random_int()

        def delayed_result1() -> int:
            time.sleep(0.1)
            return value1

        def delayed_result2() -> int:
            time.sleep(0.1)
            return value2

        result1 = Future.run(delayed_result1)
        result2 = Future.run(delayed_result2)
        result = result1.flat_map(lambda v1: result2.map(lambda v2: v1 + v2))
        time.sleep(0.2)
        assert result.is_done() is True
        assert result.get() == value1 + value2

    def test_combining_futures_with_traverse(self):
        value1 = random_int()
        value2 = random_int()

        def delayed_result1() -> int:
            time.sleep(0.1)
            return value1

        def delayed_result2() -> int:
            time.sleep(0.1)
            return value2

        result1 = Future.run(delayed_result1)
        result2 = Future.run(delayed_result2)
        result = Future.traverse([result1, result2])
        time.sleep(0.2)
        assert result.is_done() is True
        assert result.get() == [value1, value2]

    def test_on_success_success_case(self, capsys):
        value = random_int()

        def delayed_result() -> int:
            time.sleep(0.1)
            return value

        result = Future.run(delayed_result)
        result.on_success(lambda v: print(v, end=""))
        time.sleep(0.2)
        assert result.is_done() is True
        assert capsys.readouterr().out == result.value.__repr__()

    def test_on_success_fail_case(self, capsys):
        def error():
            raise RuntimeError()

        result = Future.run(error)
        result.on_success(lambda _: print(42))
        time.sleep(0.2)
        assert result.is_failure() is True
        assert not capsys.readouterr().out

    def test_on_failure_success_case(self, capsys):
        value = random_int()

        def delayed_result() -> int:
            time.sleep(0.1)
            return value

        result = Future.run(delayed_result)
        result.on_failure(print)
        time.sleep(0.2)
        assert result.is_failure() is False
        assert not capsys.readouterr().out

    def test_on_failure_fail_case(self, capsys):
        def error():
            raise RuntimeError()

        result = Future.run(error)
        result.on_failure(lambda _: print("ERROR!", end=""))
        time.sleep(0.2)
        assert result.is_failure() is True
        assert capsys.readouterr().out == "ERROR!"
