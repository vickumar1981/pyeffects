from monad import Monad


class Either(Monad):
    @staticmethod
    def of(value):
        return Right(value)

    def flat_map(self, f):
        if self.is_right():
            return f(self.value)
        else:
            return self

    def is_right(self):
        return self.biased

    def is_left(self):
        return not self.is_right()


class Left(Either):
    def __init__(self, value):
        self.value = value
        self.biased = False


class Right(Either):
    def __init__(self, value):
        self.value = value
        self.biased = True
