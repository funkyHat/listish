"""
A collection of lazy, repeatably consumable list- & tuple-like objects which
wrap any iterator.
"""

from collections import Sequence, MutableSequence


__version__ = '0.1'


class MustExhaustException(RuntimeError):
    """
    Raised when a slice cannot be converted into a list of indexes as it requires knowledge of the length of the
    iterable
    """


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
            # _consume_next will already raise StopIteration when it is
            # exhausted
            yield self._consume_next()

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = self._get_indices(index)

            min_slice = min(start, stop)
            # Add two to the max to ensure we get the last value (+1) plus the
            # fact that range() is exclusive on its stop value and requires an
            # additional +1 to cover the expected inclusive stop
            max_slice = max(start, stop) + 2
            maximum_possible_slice = range(min_slice, max_slice)
            list(self._get_items_in_bounds(maximum_possible_slice))

            return list(self._get_items_in_bounds(range(start, stop, step)))
        try:
            while len(self._datastore) < index + 1:
                self._consume_next()
            return self._datastore[index]
        except StopIteration:
            raise IndexError("index out of range")

    def _get_items_in_bounds(self, indexes):
        for i in indexes:
            try:
                yield self[i]
            except IndexError:
                return

    def _get_indices(self, slice_):
        try:
            unbounded_end = slice_.start is not None and slice_.stop is None
            unbounded_step = (
                slice_.start is None and
                slice_.stop is None and
                slice_.step is not None
            )
            negative_index = (
                (slice_.start is not None and slice_.start < 0) or
                (slice_.stop is not None and slice_.stop < 0)
            )

            if unbounded_end or unbounded_step or negative_index:
                raise MustExhaustException()

            length = max(slice_.stop, slice_.start) + 1
        except MustExhaustException:
            length = len(self)

        return slice_.indices(length)

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
