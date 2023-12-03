# -*- coding: utf-8 -*-

"""
pyeffects.Either
~~~~~~~~~~~~----

This module implements the Either, Left, and Right classes.
"""
from typing import Callable, TypeVar
from .Monad import Monad

A = TypeVar("A", covariant=True)
B = TypeVar("B")


class Either(Monad[A]):
    @staticmethod
    def of(value: B) -> "Either[B]":
        """Constructs a :class:`Either <Either>`.

        :param value: value of the new :class:`Either` object.
        :rtype: pyEffects.Either

        Usage::

          >>> from pyeffects.Either import *
          >>> Either.of(5)
          Right(5)
          >>> Right("abc")
          Right(abc)
          >>> Left(2.5)
          Left(2.5)
        """
        return Right(value)

    def flat_map(self, func: Callable[[A], "Monad[B]"]) -> "Monad[B]":
        """Flatmaps a function for :class:`Either <Either>`.

        :param func: function returning a pyEffects.Either to apply to flat_map.
        :rtype: pyEffects.Either

        Usage::

          >>> from pyeffects.Either import *
          >>> Either.of(5).flat_map(lambda v: Right(v * v))
          Right(25)
        """
        if not hasattr(func, "__call__"):
            raise TypeError("Either.flat_map expects a callable")
        if self.is_right():
            return func(self.value)
        return self  # type: ignore

    def is_right(self) -> bool:
        """Returns if the :class:`Either <Either>` is a right projection.

        :rtype: bool

        Usage::

          >>> from pyeffects.Either import *
          >>> Right(5).is_right()
          True
        """
        return self.biased

    def is_left(self) -> bool:
        """Returns if the :class:`Either <Either>` is a left projection.

        :rtype: bool

        Usage::

          >>> from pyeffects.Either import *
          >>> Right(5).is_left()
          False
        """
        return not self.is_right()

    def __eq__(self, other: object) -> bool:
        is_either_instance = isinstance(other, self.__class__)
        return (
            is_either_instance
            and self.biased == other.biased  # type: ignore
            and self.value == other.value  # type: ignore
        )


class Left(Either[A]):
    def __init__(self, value: A) -> None:
        self.value = value
        self.biased = False

    def left(self):
        return self.value

    def __str__(self) -> str:
        return "Left(" + str(self.value) + ")"

    def __repr__(self) -> str:
        return self.__str__()


class Right(Either[A]):
    def __init__(self, value: A) -> None:
        self.value = value
        self.biased = True

    def right(self):
        return self.value

    def __str__(self) -> str:
        return "Right(" + str(self.value) + ")"

    def __repr__(self) -> str:
        return self.__str__()
