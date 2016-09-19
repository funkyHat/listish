# pylint:disable=missing-docstring

import random
from sys import maxsize

from hypothesis import given, strategies
import pytest

from listish import Tupleish, Listish


def ret_(thing):
    """no-op return so we can test the classes with lists & generator inputs"""
    return thing


@pytest.mark.parametrize('cls,func', [
    (cls, func)
    for cls in [Tupleish, Listish]
    for func in [iter, ret_]
    ])
@given(l=strategies.lists(strategies.integers()))
def test_both(cls, func, l):
    gen = func(l)
    lst = cls(gen)

    max_index = 0

    for index in sorted(range(len(l)), key=lambda x: random.random()):
        max_index = max(max_index, index)

        assert lst[index] == l[index]
        assert len(lst._datastore) == max_index + 1


@pytest.mark.parametrize('cls', [Tupleish, Listish])
@given(l=strategies.lists(strategies.integers()))
def test_iter(cls, l):
    lst = cls(l)

    iterator = iter(lst)
    for value in l:
        assert next(iterator) == value

    with pytest.raises(StopIteration):
        next(iterator)


@given(
    l=strategies.lists(strategies.integers()),
    index=strategies.integers(min_value=0, max_value=maxsize),
    )
def test_insert(l, index):
    gen = l
    tup = Listish(gen)

    tup.insert(index, True)

    if index >= len(l):
        # For builtin lists, if
        # >>> l = []
        # >>> l.insert(30, True)
        # The resulting list is
        # [True]
        # Not a strange list with blank elements, so if we chose a random index
        # higher than the length of the list, we need to reset it to the top
        # element.
        index = len(l)
        assert len(tup) == len(l) + 1

    assert len(tup._datastore) == index + 1
    assert tup[index] is True
