from pyeffects.monad import Monad


class Try(Monad):
    @staticmethod
    def of(f):
        try:
            value = f()
            Success(value)
        except Exception as err:
            Failure(err)

    def flat_map(self, f):
        if self.is_success():
            return f(self.value)
        else:
            return self

    def recover(self, err, cb):
        if self.is_failure() and isinstance(self.value, err):
            return cb()
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


