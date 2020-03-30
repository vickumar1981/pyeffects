# -*- coding: utf-8 -*-

"""
pyeffects.Try
~~~~~~~~~~~~----

This module implements the Try, Success, and Faiure classes.
"""
from .Monad import Monad


class Try(Monad):
    @staticmethod
    def of(func_or_value):
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
            value = func_or_value() if hasattr(func_or_value, "__call__") else func_or_value
            return Success(value)
        except Exception as err:
            return Failure(err)

    def flat_map(self, func):
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
            return self

    def recover(self, err, recover):
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
        return self

    def recovers(self, errs, recover):
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
        return self

    def error(self):
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
            return self.value

    def is_success(self):
        """Return is success for :class:`Try <Try>`.

        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Failure(RuntimeError()).is_success()
          False
        """
        return self.biased

    def is_failure(self):
        """Return is failure for :class:`Try <Try>`.

        :rtype: pyEffects.Try

        Usage::

          >>> from pyeffects.Try import *
          >>> Failure(RuntimeError()).is_failure()
          True
        """
        return not self.is_success()


class Failure(Try):
    def __init__(self, value):
        self.value = value
        self.biased = False

    def __repr__(self):
        return 'Failure(' + str(self.value) + ')'


class Success(Try):
    def __init__(self, value):
        self.value = value
        self.biased = True

    def __repr__(self):
        return 'Success(' + str(self.value) + ')'
