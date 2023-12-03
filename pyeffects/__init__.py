# -*- coding: utf-8 -*-

"""
pyEffects Library
~~~~~~~~~~~~~~~~~
Monads for Python.  Side-effect explicitly.

Handle your side-effects in Python like a boss.  Implements functional types for Either, Option, Try, and Future.

Basic usage:
   >>> from pyeffects.Option import *
   >>> val = Some(5).map(lambda v: v * v)
   >>> val
   Some(25)
   >>> val.is_defined()
   True
   >>> val.get()
   25

:copyright: (c) 2020 by Vic Kumar.
:license: Apache 2.0, see LICENSE for more details.
"""

__version__ = "1.00.5"
