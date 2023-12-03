# -*- coding: utf-8 -*-

"""
pyeffects.Future
~~~~~~~~~~~~----

This module implements the Future class.
"""
from typing import Callable, List, TypeVar
from .Monad import Monad
from .Option import empty, Some
from .Try import Success, Failure, Try
from functools import reduce
import threading

A = TypeVar("A", covariant=True)
B = TypeVar("B")


class Future(Monad[A]):
    subscribers: List[Callable[[A], None]]

    def __init__(self, func) -> None:
        self.subscribers = []
        self.cache = empty
        self.semaphore = threading.BoundedSemaphore(1)
        self.biased = True
        self.value = None  # type: ignore
        func(self._callback)

    @staticmethod
    def of(value: B) -> "Future[B]":
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
    def _exec(func: Callable[[], A], cb: Callable[[Try[A]], None]):
        try:
            data = func()
            cb(Success(data))
        except Exception as err:
            cb(Failure(err))

    @staticmethod
    def _run_on_thread(func: Callable[[], A], cb: Callable[[Try[A]], None]):
        thread = threading.Thread(target=Future._exec, args=[func, cb])
        thread.start()

    @staticmethod
    def run(func: Callable[[], A]) -> "Future[A]":
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

    def get(self) -> A:  # type: ignore
        if self.is_success():
            return self.value.get()  # type: ignore

    def error(self) -> Exception:  # type: ignore
        if self.is_failure():
            return self.value.error()  # type: ignore

    def flat_map(self, func: Callable[[A], "Monad[B]"]) -> "Monad[B]":
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
                lambda value: cb(value) if value.is_failure() else func(value.value).on_complete(cb)  # type: ignore
            )
        )

    @staticmethod
    def traverse(arr):
        return reduce(
            lambda acc, elem: acc.flat_map(
                lambda values: elem.map(lambda value: values + [value])
            ),
            arr,
            Future.of([]),
        )

    def _callback(self, value: Try[A]) -> None:
        self.value = value  # type: ignore
        self.semaphore.acquire()
        self.cache = Some(value)  # type: ignore
        while len(self.subscribers) > 0:
            sub = self.subscribers.pop(0)
            t = threading.Thread(target=sub, args=[value])
            t.start()
        self.semaphore.release()

    def is_done(self) -> bool:
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

    def is_success(self) -> bool:
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
        return self.value and self.value.is_success()  # type: ignore

    def is_failure(self) -> bool:
        """Return is failure for :class:`Future <Future>`.

        :rtype: pyEffects.Future

        Usage::

          >>> from pyeffects.Future import *
          >>> def error():
          ...   raise RuntimeError()
          >>> Future.run(error).is_failure()
          True
        """
        return self.value and self.value.is_failure()  # type: ignore

    def on_complete(self, subscriber: Callable[[A], None]) -> None:
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

    def on_success(self, subscriber: Callable[[A], None]) -> None:
        """Calls a subscriber function when :class:`Future <Future>` completes successfully.

        :param subscriber: function to call when :class:`Future` completes successfully.

        Usage::

          >>> from pyeffects.Future import *
          >>> val = Future.of(5).map(lambda v: v * v)
          >>> val.on_success(lambda v: print(v))
          Success(25)

          >>> def error():
          ...   raise RuntimeError()
          >>> Future.run(error).on_success(lambda _: print(42))
        """
        self.semaphore.acquire()
        if self.is_failure():
            self.semaphore.release()
            return

        if self.cache.is_defined():
            self.semaphore.release()
            subscriber(self.cache.value)
        else:
            self.subscribers.append(subscriber)
            self.semaphore.release()

    def on_failure(self, subscriber: Callable[[Exception], None]) -> None:
        """Calls a subscriber function when :class:`Future <Future>` completes with error.

        :param subscriber: function to call when :class:`Future` completes with error.

        Usage::

          >>> from pyeffects.Future import *
          >>> val = Future.of(5).map(lambda v: v * v)
          >>> val.on_failure(lambda v: print(v))

          >>> def error():
          ...   raise RuntimeError()
          >>> Future.run(error).on_failure(lambda _: print('ERROR!'))
          ERROR!
        """
        self.semaphore.acquire()
        if self.is_success():
            self.semaphore.release()
            return

        if self.is_failure():
            subscriber(self.error())

        self.semaphore.release()

    def __str__(self) -> str:
        return "Future(" + str(self.value) + ")"

    def __repr__(self) -> str:
        return self.__str__()
