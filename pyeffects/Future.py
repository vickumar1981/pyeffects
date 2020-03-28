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
        func(self.callback)

    @staticmethod
    def of(value):
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
    def run(f):
        return Future(lambda cb: Future._run_on_thread(f, cb))

    def flat_map(self, func):
        return Future(
            lambda cb: self.subscribe(
                lambda value: cb(value) if value.is_failure() else func(value.value).subscribe(cb)
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
        self.value = value
        self.semaphore.acquire()
        self.cache = Some(value)
        while len(self.subscribers) > 0:
            sub = self.subscribers.pop(0)
            t = threading.Thread(target=sub, args=[value])
            t.start()
        self.semaphore.release()

    def subscribe(self, subscriber):
        self.semaphore.acquire()
        if self.cache.is_defined():
            self.semaphore.release()
            subscriber(self.cache.value)
        else:
            self.subscribers.append(subscriber)
            self.semaphore.release()
