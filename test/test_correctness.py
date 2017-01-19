import os
import sys
import doctest
from io import StringIO

import pytest
from pytest import raises

from altered import state, forget, alter, Expando

@pytest.fixture
def obj():
    return Expando(a=1)

@pytest.fixture
def dct():
    return {'a': 1}

@pytest.fixture
def objtest():
    def o_check(obj, a, b):
        assert obj.a == a
        assert obj.b == b
    return o_check

@pytest.fixture
def dcttest():
    def dct_check(dct, a, b):
        assert dct['a'] == a
        assert dct['b'] == b
    return dct_check

def test_state_obj_extra(obj):
    with state(obj, b=2, c=3):
        assert obj.b == 2
        assert obj.c == 3
    assert not hasattr(obj, 'b')
    assert not hasattr(obj, 'c')

def test_state_obj_overwrite(obj):
    with state(obj, a=2):
        assert obj.a == 2
    assert obj.a == 1

def test_state_obj_forget(obj):
    with state(obj, a=forget):
        assert not hasattr(obj, 'a')
    assert obj.a == 1

class CertainException(Exception): pass

def test_state_obj_raises(obj):
    with raises(CertainException):
        with state(obj, a=2):
            raise CertainException()
    assert obj.a == 1

def test_state_dict_extra(dct):
    with state(dct, b=2, c=3):
        assert dct == {'a':1, 'b':2, 'c':3}
    assert dct == {'a':1}

def test_state_dict_overwrite(dct):
    with state(dct, a=2):
        assert dct == {'a':2}
    assert dct == {'a':1}

def test_state_dict_forget(dct):
    with state(dct, a=forget):
        assert dct == {}
    assert dct == {'a':1}

def test_state_dct_raises(dct):
    with raises(CertainException):
        with state(dct, a=2):
            raise CertainException()
    assert dct['a'] == 1

def test_decorator_obj(obj, objtest):
    @state(obj, a=3, b=4)
    def check(o):
        objtest(o, 3, 4)
    check(obj)
    assert check.__name__ == 'check'
    assert obj.a == 1
    assert not hasattr(obj, 'b')

def test_decorator_obj_raises(obj):
    def b0rk(badness):
        @state(obj, a=2)
        def fn():
            raise badness
        fn()

    with raises(CertainException):
        b0rk(CertainException())
    assert obj.a == 1

def test_decorator_dict(dct, dcttest):
    @state(dct, a=5, b=6)
    def check(d):
        dcttest(d, 5, 6)
    check(dct)
    assert check.__name__ == 'check'
    assert dct['a'] == 1
    assert 'b' not in dct

def test_decorator_dct_raises(dct):
    def b0rk(badness):
        @state(dct, a=2)
        def fn():
            raise badness
        fn()

    with raises(CertainException):
        b0rk(CertainException())
    assert dct['a'] == 1

def test_alter_obj_extra(obj):
    restore = alter(obj, b=2, c=3)
    assert obj.b == 2
    assert obj.c == 3
    restore()
    assert not hasattr(obj, 'b')
    assert not hasattr(obj, 'c')

def test_alter_obj_overwrite(obj):
    restore = alter(obj, a=2)
    assert obj.a == 2
    restore()
    assert obj.a == 1

def test_alter_obj_forget(obj):
    restore = alter(obj, a=forget)
    assert not hasattr(obj, 'a')
    restore()
    assert obj.a == 1

def test_alter_dict_extra(dct):
    restore = alter(dct, b=2, c=3)
    assert dct == {'a': 1, 'b': 2, 'c': 3}
    restore()
    assert dct == {'a': 1}
