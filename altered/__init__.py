from __future__ import with_statement

from functools import wraps

from altered.base import (dictget, dictset, dictdel, change,
                          restore, Expando, forget)

try:
    from contextlib import ContextDecorator
except ImportError:
    from contextdecorator import ContextDecorator

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
        if isinstance(self.orig, dict):
            self.getter, self.setter, self.deleter = dictget, dictset, dictdel
        else:
            self.getter, self.setter, self.deleter = getattr, setattr, delattr
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
