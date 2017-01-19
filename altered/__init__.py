from __future__ import absolute_import
from functools import wraps

from altered.base import (dictget, dictset, dictdel, change,
                          restore, Expando, E, forget, dictlike)

try:
    from contextlib import ContextDecorator
except ImportError:
    from .contextdecorator import ContextDecorator

def changers(obj):
    """
    Chooses suitable change operations for `obj`.
    """
    return (dictlike(obj) and (dictget, dictset, dictdel) or
            (getattr, setattr, delattr) )

class state(ContextDecorator):
    """
    This combined context manager and decorator is the main API to use
    Altered States.
    """

    def __init__(self, orig, **attrs):
        self.orig = orig
        self.attrs = attrs
        return super(state, self).__init__()

    def __enter__(self):
        self.getter, self.setter, self.deleter = changers(self.orig)
        self.diff = change(self.orig, self.getter,
                           self.setter, self.deleter, **self.attrs)
        return self

    def __exit__(self, *args, **kw):
        restore(self.orig, self.diff, self.getter, self.setter, self.deleter)
        return False

    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwds):
            with self:
                return f(*args, **kwds)
        return decorated

def alter(obj, **changes):
    """
    Alternative API entry: a two step altering procedure. Same  as
    `state`, but returns a function that will restore the changes at a
    later point.
    """
    getter, setter, deleter = changers(obj)

    diff = change(obj, getter, setter, deleter, **changes)

    def restoration():
        restore(obj, diff, getter, setter, deleter)

    return restoration
