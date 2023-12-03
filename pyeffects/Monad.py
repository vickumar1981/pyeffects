from typing import Callable, Generic, TypeVar

A = TypeVar("A", covariant=True)
B = TypeVar("B")


class Monad(Generic[A]):
    value: A
    biased: bool

    @staticmethod
    def of(x: B) -> "Monad[B]":
        raise NotImplementedError("of method needs to be implemented")

    def flat_map(self, f: Callable[[A], "Monad[B]"]) -> "Monad[B]":
        raise NotImplementedError("flat_map method needs to be implemented")

    def map(self, func: Callable[[A], B]) -> "Monad[B]":
        if not hasattr(func, "__call__"):
            raise TypeError("map expects a callable")

        def wrapped(x: A) -> "Monad[B]":  # type: ignore
            return self.of(func(x))

        return self.flat_map(wrapped)

    def foreach(self, func: Callable[[A], B]) -> None:
        if not hasattr(func, "__call__"):
            raise TypeError("foreach expects a callable")
        self.map(func)

    def get(self) -> A:
        if self.biased:
            return self.value
        raise TypeError("get cannot be called on this class")

    def get_or_else(self, v: A) -> A:  # type: ignore
        if self.biased:
            return self.value
        else:
            return v

    def or_else_supply(self, func: Callable[[], A]) -> A:
        if not hasattr(func, "__call__"):
            raise TypeError("or_else_supply expects a callable")
        if self.biased:
            return self.value
        else:
            return func()

    def or_else(self, other: "Monad[A]") -> "Monad[A]":
        if not isinstance(other, Monad):
            raise TypeError("or_else can only be chained with other Monad classes")
        if self.biased:
            return self
        else:
            return other


def identity(value):
    return value
