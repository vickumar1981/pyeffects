
Using Either
============


Using the `Either Type <https://en.wikipedia.org/wiki/Union_type>`_

----------------

`Either <https://en.wikipedia.org/wiki/Union_type>`_ is a monad that represents either one thing or another thing.

An `Either` has two subclasses that hold values: `Left` and `Right`.  We can think of `Try` as a type of
`Either` where the `Left` value is always a `Failure`.  Either is a more generic version of Try, where the
left value can be anything, and not just a `Failure` class.

We can create an `Either` in three ways:

   >>> from pyeffects.Either import *
   >>> Either.of(123)
   Right(123)
   >>> Right("abc")
   Right(abc)
   >>> Left("abc")
   Left(abc)

We can also check if an `Either` is `Left` or `Right`.

   >>> from pyeffects.Either import *
   >>> v = Right("abc")
   >>> v.is_right()
   True
   >>> v.is_left()
   False

Let's say we want to convert a string to an integer, and then double the value if it is a valid integer.
We can map successful values as `Right` and invalid values to `Left`.

   >>> from pyeffects.Either import *
   >>> from pyeffects.Try import *
   >>> def to_int(s):
   ...   val = Try.of(lambda: int(s))
   ...   return Right(val) if val.is_success() else Left("age is invalid")
   ...
   >>> to_int("5")
   Right(5)
   >>> value = to_int("not an integer")
   >>> value
   Left(age is invalid)
   >>> value.is_right()
   False
   >>> value.is_left()
   True
   >>> to_int("not an integer").map(lambda v: v * 2)  # Failure does not map
   Left(age is invalid)
   >>> to_int("5").map(lambda v: v * 2)  # Map success and double value
   Right(10)

----------------

**map and flat_map**: Either is a monad and we can use `flat_map` and `map` with them.

   >>> from pyeffects.Either import *
   >>> hello = Right("Hello")
   >>> world = Right("World")
   >>> hello.flat_map(lambda h: world.map(lambda w: h + " " + w + "!"))
   Right(Hello World!)

If we try to map or flat_map on a `Left`, we get back a `Left`.

   >>> from pyeffects.Either import *
   >>> left_value = Left("Hello")
   >>> left_value.flat_map(lambda v: Right(len(v)))
   Left(Hello)

----------------

**left and right**: We can retrieve the value of an `Either` by using `left` and `right`, for `Left` and `Right` values.

   >>> from pyeffects.Either import *
   >>> left_value = Left(123)
   >>> right_value = Right("abc")
   >>> left_value.left()
   123
   >>> right_value.right()
   'abc'