
Using Futures
=============


Using the Future monad

----------------

The Future monad represents the result of an asynchronous computation that runs on another thread.

We use `Future.run` to run a function asynchronously.  Let's look at an example:

   >>> import time
   >>> from pyeffects.Future import *
   >>> import time
   >>> def delayed_result(s):
   ...   time.sleep(0.1)
   ...   return 100
   ...
   >>> result = Future.run(delayed_result).map(lambda v: v + 1)
   >>> result.is_done()
   False
   >>> time.sleep(0.2)
   >>> result.is_done()
   True
   >>> result.get()
   101

Initially, the `Future` has no value, and runs your function in the background on another thread.  Once the function
completes, the return value is supplied to the `Future` and can be retrieved using the `get()` method.

We can also create an immediate future from a value:

   >>> from pyeffects.Future.import *
   >>> val = Future.of(5).map(lambda v: v * v)
   >>> val
   Future(Success(25))

----------------

**map and flat_map**: `Future` can also use `flat_map` and `map` functions to chain operations.

   >>> from pyeffects.Future import *
   >>> hello = Future.of("Hello")
   >>> world = Future.of("World")
   >>> hello.flat_map(lambda h: world.map(lambda w: h + " " + w + "!"))
   Future(Success(Hello World!))

If we try to map or flat_map on a `Future` that has failed, we get back a failed `Future`

   >>> from pyeffects.Future import *
   >>> hello = Future.of("Hello")
   >>> failed = Future.run(lambda: int("Hello World"))  # Can't convert a string to int
   >>> hello.flat_map(lambda h: world.map(lambda w: h + " " + w + "!"))
   Future(Failure(invalid literal for int() with base 10: 'Hello World'))

----------------

**on_complete** can be used when we want to call a function when the future has completed.

   >>> from pyeffects.Future import *
   >>> Future.of("Hello World!").on_complete(lambda s: print(s))
   Success(Hello World!)