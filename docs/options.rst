
Using Option
============


Using the `Option class <https://en.wikipedia.org/wiki/Option_type>`_

----------------

A simple monad might be a container that holds either one element or zero elements.

This is the `Option class. <https://en.wikipedia.org/wiki/Option_type>`_  `Option` has two subclasses: `Some` and
`Empty`.  If the `Option` contains a value, it is `Some(value)`, otherwise it is `Empty`.

We can create an `Option` in three ways:

   >>> from pyeffects.Option import *
   >>> Option.of(123)
   Some(123)
   >>> Some("abc")
   Some(abc)
   >>> empty
   Empty()

----------------

**map and flat_map**: Options are monads, so we can use `flat_map` and `map` with them.

   >>> from pyeffects.Option import *
   >>> hello = Some("Hello")
   >>> world = Some("World")
   >>> hello.flat_map(lambda h: world.map(lambda w: h + " " + w + "!"))
   Some(Hello World!)

If we try to map or flat_map on an `Empty`, we get back an `Empty`

   >>> from pyeffects.Option import *
   >>> hello = Some("Hello")
   >>> world = empty
   >>> hello.flat_map(lambda h: world.map(lambda w: h + " " + w + "!"))
   Empty()

----------------

**get and get_or_else**: We can retrive the value of an `Option` by using `get`. However, this is unsafe.
If the `Option` is `Empty`, it will throw an exception.

   >>> from pyeffects.Option import *
   >>> v = empty
   >>> v.get()
   TypeError: get cannot be called on this class

Because of this, we try to avoid using .get wherever possible. Instead, we can use `get_or_else`. This
returns the contents of the Option if available, or a default value if it’s not.

   >>> from pyeffects.Option import *
   >>> v1 = Some("Hello")
   >>> v2 = empty
   >>> v1.get_or_else("World")
   'Hello'
   >>> v2.get_or_else("World")
   'World'

----------------

**or_else_supply and or_else**: We can chain our `Option` with a function or another `Option`,
using `or_else_supply` and `or_else` respectively.

   >>> from pyeffects.Option import *
   >>> empty.or_else_supply(lambda: "Hello World!")
   'Hello World!'
   >>> empty.or_else(Some("Hello World!"))
   'Hello World!'
