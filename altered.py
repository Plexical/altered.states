from contextlib import contextmanager

class Expando(object):

    def __init__(self, *args, **kw):
        self.update(**kw)

    def update(self, **variation):
        self.__dict__.update(variation)

    def __repr__(self):
        "Thanks Chris Jones"
        a = ', '.join('%s=%r' % i for i in self.__dict__.items())
        return '<%s object at 0x%x%s%s>' % (
                type(self).__name__, id(self), ': ' if a else '', a)


class forget: pass

def change(orig, getter, setter, deleter, **attrs):
    diff = {}
    for key, val in attrs.iteritems():
        diff[key] = getter(orig, key, forget)
        if val is forget:
            deleter(orig, key)
        else:
            setter(orig, key, val)
    return diff

def restore(orig, diff, getter, setter, deleter, **attrs):
    for key, old in diff.iteritems():
        if old is forget:
            deleter(orig, key)
        else:
            setter(orig, key, old)

def dictget(dct, key, default):
    return dct.get(key, default)

def dictset(dct, key, val):
    dct[key] = val

def dictdel(dct, key):
    del dct[key]

@contextmanager
def state(orig, getter=getattr, setter=setattr, deleter=delattr, **attrs):
    if isinstance(orig, dict):
        getter, setter, deleter = dictget, dictset, dictdel
    diff = change(orig, getter, setter, deleter, **attrs)
    yield orig
    restore(orig, diff, getter, setter, deleter, **attrs)
