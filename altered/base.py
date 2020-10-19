import os

try:
    from future import standard_library
    standard_library.install_aliases()
    from builtins import object
except ImportError:
    pass


def isenv(x):
    return x is os.environ


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
        return '<%s object at 0x%x%s%s>' % (type(self).__name__, id(self),
                                            ': ' if a else '', a)

    def __getitem__(self, key):
        "Get attribute of `Expando` via index."
        return self.__dict__[key]

    def __setitem__(self, key, val):
        "Set attribute of `Expando` via index."
        self.__dict__[key] = val

    def __delattr__(self, key):
        "Delete attribute of `Expando` via index."
        del self.__dict__[key]

    def __bool__(self):
        return bool(self.__dict__)


E = Expando


class forget(object):
    """
    Marker class to signal a value that should be deleted in an
    Altered States run.
    """


def change(orig, **attrs):
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
        diff[key] = anyget(orig, key)
        if val is forget:
            anydel(orig, key)
        else:
            anyset(orig, key, val)
    return diff


def restore(orig, diff):
    """
    Takes a diff produced by `change()` and applies it to `orig` to
    make it revert to the state it had before `change()` was called on
    it.
    """
    for key, old in diff.items():
        if old is forget:
            anydel(orig, key)
        else:
            anyset(orig, key, old)


class NoDefault:
    "Marker for not using a default value"


def anyget(x, key, default=NoDefault):
    if isenv(x):
        # os.environ have always been and still is a nasty exception
        # to all rules...
        return key in x and x[key] or forget
    try:
        return getattr(x, key)
    except AttributeError:
        try:
            return x[key]
        except KeyError:
            pass

    if default is NoDefault:
        return forget
    else:
        return default


def anyset(x, key, value):
    if isenv(x):
        # os.environ have always been and still is a nasty exception
        # to all rules... here, a setattr would not raise but wouldn't
        # update os.environ
        x[key] = value
        return
    try:
        setattr(x, key, value)
    except AttributeError:
        x[key] = value


def anydel(x, key):
    if isenv(x):
        # os.environ have always been and still is a nasty exception
        # to all rules...
        del os.environ[key]
        os.unsetenv(key)
        return

    try:
        delattr(x, key)
    except AttributeError:
        del x[key]
