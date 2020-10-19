from __future__ import absolute_import
from functools import wraps

from altered.base import (change, restore, Expando, E, forget, anyget, anyset,
                          anydel)

from altered.base import (Expando, E, forget, anyget, anyset, anydel)  # NOQA

try:
    from contextlib import ContextDecorator
except ImportError:
    from .contextdecorator import ContextDecorator


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
        self.diff = change(self.orig, **self.attrs)
        return self

    def __exit__(self, *args, **kw):
        restore(self.orig, self.diff)
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
    diff = change(obj, **changes)

    def restoration():
        restore(obj, diff)

    return restoration
