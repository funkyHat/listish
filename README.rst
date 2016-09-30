.. role:: py(code)
    :language: python
Listish
=======
.. image:: https://circleci.com/gh/funkyHat/listish.svg?style=svg
    :target: https://circleci.com/gh/funkyHat/listish

:py:`Listish` accepts an arbitrary iterable and presents it as a list-like object.
The input is used efficiently, only scanning far enough to retrieve the requested index.

.. code-block:: python

    >>> l = Listish(x for x in range(10))
    >>> l[3]
    3

Any iterable (or iterator) is supported:

.. code-block:: python

    >>> g = (x*7-1 for x in [6,2,1,7,9,33])
    >>> l = Listish(g)
    >>> l[3]
    48
