from .monad import Monad
from .option import empty, Some
from .either import Either, Left, Right
from functools import reduce
import threading


class Future(Monad):
    def __init__(self, func):
        self.subscribers = []
        self.cache = empty
        self.semaphore = threading.BoundedSemaphore(1)
        func(self.callback)

    @staticmethod
    def of(value):
        return Future(lambda callback: callback(Either.of(value)))

    @staticmethod
    def run(function, callback):
        try:
            data = function()
            callback(Right(data))
        except Exception as err:
            callback(Left(err))

    @staticmethod
    def run_on_thread(func, callback):
        thread = threading.Thread(target=Future.run, args=[func, callback])
        thread.start()

    @staticmethod
    def run_async(f):
        return Future(lambda callback: Future.run_on_thread(f, callback))

    def flat_map(self, func):
        return Future(
            lambda callback: self.subscribe(
                lambda value: func(value.value).subscribe(callback) if value.biased else callback(value)
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

    def callback(self, value):
        self.semaphore.acquire()
        self.cache = Some(value)
        while len(self.subscribers) > 0:
            sub = self.subscribers.pop(0)
            t = threading.Thread(target=sub, args=[value])
            t.start()
        self.semaphore.release()

    def subscribe(self, subscriber):
        self.semaphore.acquire()
        if self.cache.defined:
            self.semaphore.release()
            subscriber(self.cache.value)
        else:
            self.subscribers.append(subscriber)
            self.semaphore.release()
