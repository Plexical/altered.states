from contextlib import contextmanager
from functools import wraps

try:
    from contextlib import ContextDecorator
except ImportError:
    from contextdecorator import ContextDecorator

class Expando(object):
    """
    A completely promiscous object that makes attributes out of
    key/value parameters to it's `__init__()` method.
    """

    def __init__(self, *args, **kw):
        self.update(**kw)

    def update(self, **variation):
        """
        Writes over arbitrary attributes in the `Expando` object, same
        semantics as `dict.update()`.
        """
        self.__dict__.update(variation)

    def __repr__(self):
        """
        Writes out all attributes of the object.

        Thanks Chris Jones
        """
        a = ', '.join('%s=%r' % i for i in self.__dict__.items())
        return '<%s object at 0x%x%s%s>' % (
                type(self).__name__, id(self), ': ' if a else '', a)


class forget:
    """
    Marker class to signal a value that should be deleted in an
    Altered States run.
    """

def change(orig, getter, setter, deleter, **attrs):
    """
    Alter `orig` using the functions `getter`, `setter` and `deleter`
    with the contents of `**attrs`. The get/set/delete use the same
    semantics as standard `getattr`/`setattr` and `delattr`.

    While `change()` alters `orig` it also builds a diff of what it
    has done to later be passed to `restore()` to reset `orig` till
    it's original state.
    """
    diff = {}
    for key, val in attrs.iteritems():
        diff[key] = getter(orig, key, forget)
        if val is forget:
            deleter(orig, key)
        else:
            setter(orig, key, val)
    return diff

def restore(orig, diff, getter, setter, deleter):
    """
    Takes a diff produced by `change()` and applies it to `orig` to
    make it revert to the state it had before `change()` was called on
    it.
    """
    for key, old in diff.iteritems():
        if old is forget:
            deleter(orig, key)
        else:
            setter(orig, key, old)

def dictget(dct, key, default):
    "Provides `getattr` semantics for modifying dictionaries."
    return dct.get(key, default)

def dictset(dct, key, val):
    "Provides `setattr` semantics for modifying dictionaries."
    dct[key] = val

def dictdel(dct, key):
    "Provides `delattr` semantics for modifiyng dictionaries."
    del dct[key]

class state(ContextDecorator):

    def __new__(self, orig, **attrs):
        self.orig = orig
        self.attrs = attrs
        return ContextDecorator.__new__(self)

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
