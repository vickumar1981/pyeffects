
Using Try
=========


Using the Try monad

----------------

Let's take look at how we approach error handling with exceptions.

We might raise an error when some unexpected behavior occurs, e.g.:

   >>> def check_age(age):
   ...   if age <= 15:
   ...     raise ValueError("age must be >= 15")
   ...
   >>> check_age(10)
   ValueError("age must be >= 15")

Having this kind of exception handling code in your code base can increase its complexity
very quickly and can make debugging programs harder.  It is preferable to signify that an error
has occured by returning an appropriate value from your function.

Just like `Option` had two subtypes: `Some` and `Empty`, `Try` also has two subclasses.  If a computation
is successful, the result is a `Success` which wraps the return value.  If it throws an exception, then
the error is wrapped in a `Failure` class.

If we know the a computation may result in an error, we can use `Try` as the return type of our function.
This makes the return type explicit and forces clients of our function to deal with the possibility of an
error.

For example, say we want to convert a string to an integer, and then double the value.

   >>> from pyeffects.Try import *
   >>> def to_int(s):
   ...   return Try.of(lambda: int(s))
   >>> to_int("5")
   Success(5)
   >>> to_int("not an integer")
   Failure(invalid literal for int() with base 10: 'not an integer')
   >>> to_int("5").map(lambda v: v * 2)
   Success(10)

----------------


Try Operations
==============

**map and flat_map**: Chaining operations together

   >>> from pyeffects.Try import *
   >>> hello = Success("Hello")
   >>> world = Success("World")
   >>> hello.flat_map(lambda h: world.map(lambda w: h + " " + w + "!"))
   Success(Hello World!)

----------------

**recover and recovers** can be used to recover from errors and exceptions.

   >>> def check_age(age):
   ...   if age <= 15:
   ...     raise ValueError("age must be >= 15")
   ...
   >>> def default_age():
   ...   return 18
   ...
   >>> Try.of(lambda: check_age(10)).recover(ValueError, default_age)
   Success(18)
   >>> Try.of(lambda: check_age(10)).recovers([ValueError, OverflowError], "no age")
   Success(no age)

----------------

**get and get_or_else**: We can retrieve the value of an `Try` by using `get` and `get_or_else`.

   >>> from pyeffects.Try import *
   >>> v1 = Success("Hello")
   >>> v1.get()
   'Hello'
   >>> v2 = Failure(RuntimeError())
   >>> v2.get_or_else("World")
   'World'

----------------

**or_else_supply and or_else**: We can also supply a value if our 'Try' has failed by using a function or another `Try`,
using `or_else_supply` and `or_else` respectively.

   >>> from pyeffects.Try import *
   >>> Failure(Exception()).or_else_supply(lambda: "Hello World!")
   'Hello World!'
   >>> Failure(Exception()).or_else(Success("Hello World!"))
   Success(Hello World!)

----------------

**foreach** can be used when we want to apply a function, but unlike with `map`, we don't care about the return value.

   >>> from pyeffects.Try import *
   >>> Success("Hello World!").foreach(lambda s: print(s))
   'Hello World!'
