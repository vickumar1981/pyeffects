# -*- coding: utf-8 -*-

"""
pyeffects.Try
~~~~~~~~~~~~----

This module implements the Try, Success, and Faiure classes.
"""
from typing import Callable, List, Type, TypeVar, Union
from .Monad import Monad

A = TypeVar("A", covariant=True)
B = TypeVar("B")


class Try(Monad[A]):
    @staticmethod
    def of(func_or_value: Union[B, Callable[[], B]]) -> "Try[B]":
        """Constructs a :class:`Try <Try>`.

        :param func_or_value: function or value to construct a new :class:`Try` object
        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Try.of(lambda: 5)
          Success(5)
          >>> Try.of("abc")
          Success(abc)
          >>> def error():
          ...   raise Exception("failed")
          ...
          >>> Try.of(error)
          Failure(failed)
        """
        try:
            value = func_or_value() if hasattr(func_or_value, "__call__") else func_or_value  # type: ignore
            return Success(value)  # type: ignore
        except Exception as err:
            return Failure(err)

    def flat_map(self, func: Callable[[A], "Monad[B]"]) -> "Monad[B]":
        """Flatmaps a function for :class:`Try <Try>`.

        :param func: function returning a pyEffects.Try to apply to flat_map.
        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Success(5).flat_map(lambda v: Success(v * v))
          Success(25)
        """
        if not hasattr(func, "__call__"):
            raise TypeError("Try.flat_map expects a callable")
        if self.is_success():
            return func(self.value)
        else:
            return self  # type: ignore

    def recover(
        self, err: Type[Exception], recover: Union[B, Callable[[], B]]
    ) -> "Try[B]":
        """Recover from an exception for :class:`Try <Try>`.

        :param err: The class of exception to recover from.
        :param recover: The function to apply when recovering from an exception
        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> def error():
          ...   raise RuntimeError("failed")
          ...
          >>> Try.of(error).recover(RuntimeError, "abc")
          Success(abc)
        """
        if self.is_failure() and isinstance(self.value, err):
            return Try.of(recover)
        return self  # type: ignore

    def recovers(
        self, errs: List[Type[Exception]], recover: Union[B, Callable[[], B]]
    ) -> "Try[B]":
        """Recover from an exception for :class:`Try <Try>`.

        :param errs: A list of classes of exceptions to recover from.
        :param recover: The function to apply when recovering from an exception
        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> def error():
          ...   raise RuntimeError("failed")
          ...
          >>> Try.of(error).recovers([RuntimeError, NotImplementedError], "abc")
          Success(abc)
        """
        if not isinstance(errs, list):
            raise TypeError("Try.recovers expects a list of errors as the 1nd arg")
        if self.is_failure() and any([isinstance(self.value, e) for e in errs]):
            return Try.of(recover)
        return self  # type: ignore

    def error(self) -> Exception:  # type: ignore
        """Recover the exception for :class:`Try <Try>`.

        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> def error():
          ...  raise RuntimeError()
          ...
          >>> Try.of(error).error()
          RuntimeError()
        """
        if self.is_failure():
            return self.value  # type: ignore

    def is_success(self) -> bool:
        """Return is success for :class:`Try <Try>`.

        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Failure(RuntimeError()).is_success()
          False
        """
        return self.biased

    def is_failure(self) -> bool:
        """Return is failure for :class:`Try <Try>`.

        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Failure(RuntimeError()).is_failure()
          True
        """
        return not self.is_success()

    def on_success(self, func: Callable[[A], None]) -> None:
        """Calls a function on success.

        :rtype pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Try.of('abc').on_success(print)
          abc
        """

        if self.is_success():
            func(self.value)

    def on_failure(self, func: Callable[[Exception], None]) -> None:
        """Calls a function on failure.

        :rtype pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Failure(RuntimeError('Error!')).on_failure(print)
          Error!
        """

        if self.is_failure():
            func(self.error())

    def __eq__(self, other: object) -> bool:
        is_try_instance = isinstance(other, self.__class__)
        return (
            is_try_instance
            and self.biased == other.biased  # type: ignore
            and self.value == other.value  # type: ignore
        )


class Failure(Try[A]):
    def __init__(self, value: Exception) -> None:
        self.value = value  # type: ignore
        self.biased = False

    def __str__(self) -> str:
        return "Failure(" + str(self.value) + ")"

    def __repr__(self) -> str:
        return self.__str__()


class Success(Try[A]):
    def __init__(self, value: A) -> None:
        self.value = value
        self.biased = True

    def __str__(self) -> str:
        return "Success(" + str(self.value) + ")"

    def __repr__(self) -> str:
        return self.__str__()
