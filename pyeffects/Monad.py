class Monad:
    @staticmethod
    def of(x):
        raise NotImplementedError("of method needs to be implemented")

    def flat_map(self, f):
        raise NotImplementedError("flat_map method needs to be implemented")

    def map(self, f):
        return self.flat_map(lambda x: self.of(f(x)))

    def get(self):
        if self.biased:
            return self.value
        raise TypeError("get() cannot be called on this class")

    def get_or_else(self, v):
        if self.biased:
            return self.value
        else:
            return v

    def or_else_supply(self, f):
        if self.biased:
            return self.value
        else:
            return f()

    def or_else(self, other):
        if self.biased:
            return self
        else:
            return other


def identity(value):
    return value
