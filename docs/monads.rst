
What is a Monad?
================


What is a `Monad <https://en.wikipedia.org/wiki/Monad_(functional_programming)>`_ and when to use it?

----------------

`A Monad is a container. <https://en.wikipedia.org/wiki/Monad_(functional_programming)>`_

A Monad contains elements, but instead of operating on those elements directly, the container has properties
and functions that allow us to work with the elements inside of it.  These are often called higher-order functions,
because they take another function as an input parameter.  Typically, a monad has two very important higher-order
functions called `map` and `flat_map`.

`More on map and flat_map <https://pyeffects.readthedocs.io/en/latest/map_and_flatmap.html>`_

.. image:: https://porizi.files.wordpress.com/2014/02/monad-transformations.png

Often, a complex tasks has several steps, and this can result in very complex code. We might have callbacks,
multiple functions that pass results back and forth, conditional trees, or other kinds of sticky patterns,
that result in greater complexity and more time spent debugging.

We often want to take a complex problem and break it down into smaller tasks, and then put
those tasks back together to solve a problem. We can reduce the complexity by breaking down a problem,
and letting each individual part of the process take care of its own responsibility, and then passing
the result onto the next part in the chain. We want to break down our problem into a number of small
functions, and then compose those functions together into one function that represents the entire task.

Composing functions is the reason why we want to use monads. We can create a container that can perform
actions on its contents, and then use the container as a way to manage those contents and perform the
actions we need, in the order we need to, encapsulating our operations via function composition.
Instead of handling the objects and outputs of functions, we put the objects into a container, and then
write up a manifest of all the functions we need done to it. Like an assembly line, we put the
raw materials in one end and get the finished product from the other end.

When we create a Monad, we’re essentially building an assembly line out of individual assembly line
components (functions) that can handle raw materials of various types. When we execute our code,
we’re feeding raw materials (values) into the assembly line and watching it operate,
eventually spitting out a finished product.
