try:
    from future import standard_library
    standard_library.install_aliases()
    from builtins import object
except ImportError:
    pass

import collections

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
        a = ', '.join('%s=%r' % i for i in list(self.__dict__.items()))
        return '<%s object at 0x%x%s%s>' % (
                type(self).__name__, id(self), ': ' if a else '', a)

    def __bool__(self):
        return bool(self.__dict__)

E = Expando

class forget(object):
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
    for key, val in attrs.items():
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
    for key, old in diff.items():
        if old is forget:
            deleter(orig, key)
        else:
            setter(orig, key, old)

def dictlike(cand):
    "Determines if `dict` or `object` semantics should be used"
    return isinstance(cand, collections.Mapping)

def dictget(dct, key, default):
    "Provides `getattr` semantics for modifying dictionaries."
    return dct.get(key, default)

def dictset(dct, key, val):
    "Provides `setattr` semantics for modifying dictionaries."
    dct[key] = val

def dictdel(dct, key):
    "Provides `delattr` semantics for modifiyng dictionaries."
    del dct[key]

