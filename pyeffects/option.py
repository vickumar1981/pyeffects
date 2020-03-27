from pyeffects.monad import Monad


class Option(Monad):
    @staticmethod
    def of(x):
        return Some(x)

    def flat_map(self, f):
        if self.is_defined():
            return f(self.value)
        else:
            return empty

    def is_defined(self):
        return self.biased

    def is_empty(self):
        return not self.is_defined()


class Some(Option):
    def __init__(self, value):
        self.value = value
        self.biased = True


class Empty(Option):
    def __init__(self):
        self.value = None
        self.biased = False


empty = Empty()
