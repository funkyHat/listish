.. role:: py(code)
    :language: python

Listish
=======
.. image:: https://circleci.com/gh/funkyHat/listish.svg?style=svg
    :target: https://circleci.com/gh/funkyHat/listish

:py:`listish.Listish` is a list-behaviour wrapper for arbitrary sequences and iterables (including iterators).

It acts as a mutable data wrapper for arbitrary inputs.
On top of non-indexable input it also adds indexability.


Any iterable (or iterator) is supported:

.. code-block:: python

    >>> g = (x*7-1 for x in [6,2,1,7,9,33])
    >>> l = Listish(g)
    >>> l[3]
    48
    

Complex slicing is supported:

.. code-block:: python

    >>> l = Listish(x for x in range(100) if x % 3)
    >>> l[0:20:2]
    [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]
    

The input is used somewhat efficiently,
only scanning far enough to retrieve the requested index:

.. code-block:: python

    >>> r = (x for x in range(10))
    >>> l = Listish(r)
    >>> l[4]
    4
    >>> next(r)
    5

.. note::
    In practise interfering with an iterable after passing it to this library is a bad idea,
    as we can see, continuing in the same ``python`` session:

    .. code-block:: python

        >>> l[5]
        6


Tupleish
========
:py:`listish.Tupleish` provides indexing & persistence while presenting an immutable interface.
:py:`listish.Listish` inherits most of its functionality from :py:`listish.Tupleish`,
which is provided as a separate class for some kind of completeness.


See Also
========
:py:`itertools.tee`, in the standard library, provides ``n`` iterables which proxy the same input iterable, while using the minimum required memory, which may be more suitable for some use cases than :py:`Listish` or :py:`Tupleish`, though it does not attempt to add enumerability or mutability.
