from monad import Monad
from option import empty, Some
from either import Either, Left, Right
from functools import reduce
import threading


class Future(Monad):
    def __init__(self, f):
        self.subscribers = []
        self.cache = empty
        self.semaphore = threading.BoundedSemaphore(1)
        f(self.callback)

    @staticmethod
    def of(value):
        return Future(lambda cb: cb(Either.of(value)))

    @staticmethod
    def exec(f, cb):
        try:
            data = f()
            cb(Right(data))
        except Exception as err:
            cb(Left(err))

    @staticmethod
    def exec_on_thread(f, cb):
        t = threading.Thread(target=Future.exec, args=[f, cb])
        t.start()

    @staticmethod
    def run_async(f):
        return Future(lambda cb: Future.exec_on_thread(f, cb))

    def flat_map(self, f):
        return Future(
            lambda cb: self.subscribe(
                lambda value: f(value.value).subscribe(cb) if value.biased else cb(value)
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