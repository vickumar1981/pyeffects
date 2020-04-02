Map and Flat Map
================

`map` takes in a function (A -> B) where A and B are any type.

For example:
   >>> from pyeffects.Option import  *
   >>> Some("abc").map(lambda s: len(s))
   Some(3)

.. image:: https://porizi.files.wordpress.com/2014/02/map.png

`flat_map` takes in a function (A -> M[B]) where A and B are any types and M is the container.

For example:
   >>> from pyeffects.Option import  *
   >>> Some("abc").flat_map(lambda s: Some(len(s)))
   Some(3)

.. image:: https://porizi.files.wordpress.com/2014/02/flatmap.png

`flat_map` is a more general version of the `map` function.

Both operations return a container of type B.