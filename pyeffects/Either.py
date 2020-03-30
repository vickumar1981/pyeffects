# -*- coding: utf-8 -*-

"""
pyeffects.Either
~~~~~~~~~~~~----

This module implements the Either, Left, and Right classes.
"""
from .Monad import Monad


class Either(Monad):
    @staticmethod
    def of(value):
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

    def flat_map(self, func):
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
        return self

    def is_right(self):
        """Returns if the :class:`Either <Either>` is a right projection.

        :rtype: bool

        Usage::

          >>> from pyeffects.Either import *
          >>> Right(5).is_right()
          True
        """
        return self.biased

    def is_left(self):
        """Returns if the :class:`Either <Either>` is a left projection.

        :rtype: bool

        Usage::

          >>> from pyeffects.Either import *
          >>> Right(5).is_left()
          False
        """
        return not self.is_right()


class Left(Either):
    def __init__(self, value):
        self.value = value
        self.biased = False

    def left(self):
        return self.value

    def __repr__(self):
        return 'Left(' + str(self.value) + ')'


class Right(Either):
    def __init__(self, value):
        self.value = value
        self.biased = True

    def right(self):
        return self.value

    def __repr__(self):
        return 'Right(' + str(self.value) + ')'
