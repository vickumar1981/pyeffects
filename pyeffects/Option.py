# -*- coding: utf-8 -*-

"""
pyeffects.Option
~~~~~~~~~~~~----

This module implements the Option, Some, and Empty classes.
"""
from .Monad import Monad


class Option(Monad):
    @staticmethod
    def of(value):
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

    def flat_map(self, func):
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

    def is_defined(self):
        """Returns if the :class:`Option <Option>` is defined or not.

        :rtype: bool

        Usage::

          >>> from pyeffects.Option import *
          >>> Some(5).is_defined()
          True
        """
        return self.biased

    def is_empty(self):
        """Returns if the :class:`Option <Option>` is empty or not.

        :rtype: bool

        Usage::

          >>> from pyeffects.Option import *
          >>> Some(5).is_empty()
          False
        """
        return not self.is_defined()


class Some(Option):
    def __init__(self, value):
        self.value = value
        self.biased = True

    def __repr__(self):
        return 'Some(' + str(self.value) + ')'


class Empty(Option):
    def __init__(self):
        self.value = None
        self.biased = False

    def __repr__(self):
        return 'Empty()'


empty = Empty()
