# -*- coding: utf-8 -*-

"""
pyeffects.Option
~~~~~~~~~~~~----

This module implements the Option, Some, and Empty classes.
"""
from typing import Callable, TypeVar
from .Monad import Monad

A = TypeVar("A", covariant=True)
B = TypeVar("B")


class Option(Monad[A]):
    @staticmethod
    def of(value: B) -> "Option[B]":
        """Constructs a :class:`Option <Option>`.

        :param value: value of the new :class:`Option` object.
        :rtype: pyEffects.Option

        Usage::

          >>> from pyeffects.Option import *
          >>> Option.of(5)
          Some(5)
          >>> Option.of("abc")
          Some(abc)
          >>> Option.of(None)
          Empty()
        """
        return empty if value is None else Some(value)

    def flat_map(self, func: Callable[[A], "Monad[B]"]) -> "Monad[B]":
        """Flatmaps a function for :class:`Option <Option>`.

        :param func: function returning a pyEffects.Option to apply to flat_map.
        :rtype: pyEffects.Option

        Usage::

          >>> from pyeffects.Option import *
          >>> Some(5).flat_map(lambda v: Some(v * v))
          Some(25)
        """
        if not hasattr(func, "__call__"):
            raise TypeError("Option.flat_map expects a callable")
        if self.is_defined():
            return func(self.value)
        else:
            return empty

    def is_defined(self) -> bool:
        """Returns if the :class:`Option <Option>` is defined or not.

        :rtype: bool

        Usage::

          >>> from pyeffects.Option import *
          >>> Some(5).is_defined()
          True
        """
        return self.biased

    def is_empty(self) -> bool:
        """Returns if the :class:`Option <Option>` is empty or not.

        :rtype: bool

        Usage::

          >>> from pyeffects.Option import *
          >>> Some(5).is_empty()
          False
        """
        return not self.is_defined()

    def __eq__(self, other: object) -> bool:
        is_option_instance = isinstance(other, self.__class__)
        return (
            is_option_instance
            and self.biased == other.biased  # type: ignore
            and self.value == other.value  # type: ignore
        )


class Some(Option[A]):
    def __init__(self, value: A) -> None:
        self.value = value
        self.biased = True

    def __str__(self) -> str:
        return "Some(" + str(self.value) + ")"

    def __repr__(self) -> str:
        return self.__str__()


class Empty(Option[A]):
    def __init__(self) -> None:
        self.value = None  # type: ignore
        self.biased = False

    def __str__(self) -> str:
        return "Empty()"

    def __repr__(self) -> str:
        return self.__str__()


empty = Empty()  # type: ignore
