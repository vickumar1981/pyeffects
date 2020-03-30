class Monad:
    @staticmethod
    def of(x):
        raise NotImplementedError("of method needs to be implemented")

    def flat_map(self, f):
        raise NotImplementedError("flat_map method needs to be implemented")

    def map(self, func):
        if not hasattr(func, "__call__"):
            raise TypeError("map expects a callable")
        return self.flat_map(lambda x: self.of(func(x)))

    def foreach(self, func):
        if not hasattr(func, "__call__"):
            raise TypeError("map expects a callable")
        self.map(func)

    def get(self):
        if self.biased:
            return self.value
        raise TypeError("get cannot be called on this class")

    def get_or_else(self, v):
        if self.biased:
            return self.value
        else:
            return v

    def or_else_supply(self, func):
        if not hasattr(func, "__call__"):
            raise TypeError("or_else_supply expects a callable")
        if self.biased:
            return self.value
        else:
            return func()

    def or_else(self, other):
        if not isinstance(other, Monad):
            raise TypeError("or_else can only be chained with other Monad classes")
        if self.biased:
            return self
        else:
            return other


def identity(value):
    return value
