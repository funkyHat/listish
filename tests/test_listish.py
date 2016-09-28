# pylint:disable=missing-docstring

import random
from sys import maxsize

import pytest
from hypothesis import given, strategies

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


@pytest.mark.parametrize('cls', [Tupleish, Listish])
@given(l=strategies.lists(strategies.integers(), min_size=1))
def test_iter_twice(cls, l):
    lst = cls(l)
    # Iterate over the first element so it's pre-cached
    next(iter(lst))

    iterator = iter(lst)
    for value in l:
        assert next(iterator) == value


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


@strategies.composite
def list_and_index(draw, elements=strategies.integers()):
    xs = draw(strategies.lists(elements, min_size=1))
    i = draw(strategies.integers(min_value=0, max_value=len(xs) - 1))
    return xs, i


@strategies.composite
def list_and_indexerror(draw, elements=strategies.integers()):
    xs = draw(strategies.lists(elements))
    i = draw(strategies.integers(min_value=len(xs)))
    return xs, i


@given(li=list_and_index())
def test_setitem(li):
    l, i = li
    lst = Listish(l)

    lst[i] = True

    assert lst[i] is True


@given(li=list_and_indexerror())
def test_setitem_indexerror(li):
    l, i = li
    lst = Listish(l)

    with pytest.raises(IndexError) as e:
        lst[i] = True
    assert 'assignment' in str(e.value)


@given(li=list_and_index())
def test_delitem(li):
    l, i = li
    lst = Listish(l)

    del lst[i]

    lst_list = list(lst)

    assert len(lst_list) == len(l) - 1


@given(li=list_and_indexerror())
def test_delitem_indexerror(li):
    l, i = li
    lst = Listish(l)

    with pytest.raises(IndexError) as e:
        del lst[i]
    assert 'assignment' in str(e.value)
