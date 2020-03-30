# -*- coding: utf-8 -*-

"""
pyeffects.Future
~~~~~~~~~~~~----

This module implements the Future class.
"""
from .Monad import Monad
from .Option import empty, Some
from .Try import Success, Failure
from functools import reduce
import threading


class Future(Monad):
    def __init__(self, func):
        self.subscribers = []
        self.cache = empty
        self.semaphore = threading.BoundedSemaphore(1)
        self.biased = True
        self.value = None
        func(self._callback)

    @staticmethod
    def of(value):
        """Constructs an immediate :class:`Future <Future>`.

        :param value: value of the new :class:`Future` object.
        :rtype: pyEffects.Future

        Usage::

          >>> from pyeffects.Future import *
          >>> Future.of(5)
          Future(Success(5))
          >>> Future.of("abc")
          Future(Success(abc))
        """
        return Future(lambda cb: cb(Success(value)))

    @staticmethod
    def _exec(func, cb):
        try:
            data = func()
            cb(Success(data))
        except Exception as err:
            cb(Failure(err))

    @staticmethod
    def _run_on_thread(func, cb):
        thread = threading.Thread(target=Future._exec, args=[func, cb])
        thread.start()

    @staticmethod
    def run(func):
        """Constructs a :class:`Future <Future>` that runs asynchronously on another thread.

        :param func: function to run on new thread and return a new :class:`Future` object
        :rtype: pyEffects.Future

        Usage::

          >>> import time
          >>> from pyeffects.Future import *
          >>> def get_value():
          ...   time.sleep(1)
          ...   return "abc"
          ...
          >>> Future.run(get_value)
          Future(None)
        """
        if not hasattr(func, "__call__"):
            raise TypeError("Future.run expects a callable")
        return Future(lambda cb: Future._run_on_thread(func, cb))

    def get(self):
        if self.is_success():
            return self.value.get()

    def error(self):
        if self.is_failure():
            return self.value.error()

    def flat_map(self, func):
        """Flatmaps a function for :class:`Future <Future>`.

        :param func: function returning a pyEffects.Future to apply to flat_map.
        :rtype: pyEffects.Future

        Usage::

          >>> from pyeffects.Future import *
          >>> Future.of(5).flat_map(lambda v: Future.of(v * v))
          Future(Success(25))
        """
        if not hasattr(func, "__call__"):
            raise TypeError("Future.flat_map expects a callable")
        return Future(
            lambda cb: self.on_complete(
                lambda value: cb(value) if value.is_failure() else func(value.value).on_complete(cb)
            )
        )

    @staticmethod
    def traverse(arr):
        return lambda f: reduce(
            lambda acc, elem: acc.flat_map(
                lambda values: f(elem).map(
                    lambda value: values + [value]
                )
            ), arr, Future.of([]))

    def _callback(self, value):
        self.value = value
        self.semaphore.acquire()
        self.cache = Some(value)
        while len(self.subscribers) > 0:
            sub = self.subscribers.pop(0)
            t = threading.Thread(target=sub, args=[value])
            t.start()
        self.semaphore.release()

    def is_done(self):
        """Return is done for :class:`Future <Future>`.

        :rtype: pyEffects.Future

        Usage::

          >>> import time
          >>> from pyeffects.Future import *
          >>> def wait_for_result():
          ...   time.sleep(0.2)
          ...   return "abc"
          ...
          >>> Future.run(wait_for_result).is_done()
          False
        """
        return self.value is not None

    def is_success(self):
        """Return is success for :class:`Future <Future>`.

        :rtype: pyEffects.Future

        Usage::

          >>> from pyeffects.Future import *
          >>> def error():
          ...   raise RuntimeError()
          ...
          >>> Future.run(error).is_success()
          False
        """
        return self.value and self.value.is_success()

    def is_failure(self):
        """Return is failure for :class:`Future <Future>`.

        :rtype: pyEffects.Future

        Usage::

          >>> from pyeffects.Future import *
          >>> def error():
          ...   raise RuntimeError()
          >>> Future.run(error).is_failure()
          True
        """
        return self.value and self.value.is_failure()

    def on_complete(self, subscriber):
        """Calls a subscriber function when :class:`Future <Future>` completes.

        :param subscriber: function to call when :class:`Future` completes.

        Usage::

          >>> from pyeffects.Future import *
          >>> val = Future.of(5).flat_map(lambda v: Future.of(v * v))
          >>> val
          Future(Success(25))
          >>> val.on_complete(lambda v: print(v))
          Success(25)
        """
        self.semaphore.acquire()
        if self.cache.is_defined():
            self.semaphore.release()
            subscriber(self.cache.value)
        else:
            self.subscribers.append(subscriber)
            self.semaphore.release()

    def __repr__(self):
        return 'Future(' + str(self.value) + ')'
