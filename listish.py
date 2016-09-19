"""
A collection of lazy, repeatably consumable list- & tuple-like objects which
wrap any iterator.
"""

from collections import Sequence, MutableSequence


class Tupleish(Sequence):
    """
    A lazily evaluated tuple-like object.
    """

    def __init__(self, iterable):
        # iter(iterator) returns the iterator
        self._iterator = iter(iterable)
        self._datastore = []

    def _consume_next(self):
        value = next(self._iterator)
        self._datastore.append(value)
        return value

    def __iter__(self):
        for value in self._datastore:
            yield value
        while True:
            # _consume_next will alread raise StopIteration when it is
            # exhausted
            yield self._consume_next()

    def __getitem__(self, index):
        try:
            while len(self._datastore) < index + 1:
                self._consume_next()
            return self._datastore[index]
        except StopIteration:
            raise IndexError("index out of range")

    def __len__(self):
        self._datastore += list(self._iterator)
        return len(self._datastore)


class Listish(Tupleish, MutableSequence):
    """
    A lazily evaluated list-like object.
    """

    def __setitem__(self, index, value):
        try:
            self[index]
        except IndexError:
            raise IndexError("assignment index out of range")
        self._datastore[index] = value

    def __delitem__(self, index):
        try:
            self[index]
        except IndexError:
            raise IndexError("assignment index out of range")
        del self._datastore[index]

    def insert(self, index, value):
        if index == 0:
            self._datastore = [value] + self._datastore
        else:
            try:
                self[index - 1]
            except IndexError:
                pass
            self._datastore.insert(index, value)
