from .monad import Monad


class Try(Monad):
    @staticmethod
    def of(func):
        try:
            value = func()
            Success(value)
        except Exception as err:
            Failure(err)

    def flat_map(self, func):
        if self.is_success():
            return func(self.value)
        else:
            return self

    def recover(self, err, callback):
        if self.is_failure() and isinstance(self.value, err):
            return callback()
        else:
            return self

    def error(self):
        if self.is_failure():
            return self.value

    def is_success(self):
        return self.biased

    def is_failure(self):
        return not self.is_success()


class Failure(Try):
    def __init__(self, value):
        self.value = value
        self.biased = False


class Success(Try):
    def __init__(self, value):
        self.value = value
        self.biased = True
