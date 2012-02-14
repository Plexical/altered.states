from __future__ import with_statement

import pytest

from altered import state, forget, Expando

pytest_funcarg__obj = lambda request: Expando(a=1)
pytest_funcarg__dct = lambda request: {'a':1}

def pytest_funcarg__objtest(request):
    def o_check(obj, a, b):
        assert obj.a == a
        assert obj.b == b
    return o_check

def pytest_funcarg__dcttest(request):
    def dct_check(dct, a, b):
        assert dct['a'] == a
        assert dct['b'] == b
    return dct_check

# @state(os.environ, DJANGO_SETTINGS_MODULE='proj.settings')
# def test_django_case():
#     # ...

def test_state_obj_extra(obj):
    with(state(obj, b=2, c=3)):
        assert obj.b == 2
        assert obj.c == 3
    assert not hasattr(obj, 'b')
    assert not hasattr(obj, 'c')

def test_state_obj_overwrite(obj):
    with(state(obj, a=2)):
        assert obj.a == 2
    assert obj.a == 1

def test_state_obj_forget(obj):
    with(state(obj, a=forget)):
        assert not hasattr(obj, 'a')
    assert obj.a == 1

def test_state_dict_extra(dct):
    with(state(dct, b=2, c=3)):
        assert dct == {'a':1, 'b':2, 'c':3}
    assert dct == {'a':1}

def test_state_dict_overwrite(dct):
    with(state(dct, a=2)):
        assert dct == {'a':2}
    assert dct == {'a':1}

def test_state_dict_forget(dct):
    with(state(dct, a=forget)):
        assert dct == {}
    assert dct == {'a':1}

def test_decorator_obj(obj, objtest):
    @state(obj, a=3, b=4)
    def check(o):
        objtest(o, 3, 4)
    check(obj)
    assert check.func_name == 'check'
    assert obj.a == 1
    assert not hasattr(obj, 'b')

def test_decorator_dict(dct, dcttest):
    @state(dct, a=5, b=6)
    def check(d):
        dcttest(d, 5, 6)
    check(dct)
    assert check.func_name == 'check'
    assert dct['a'] == 1
    assert 'b' not in dct
