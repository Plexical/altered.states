=================
 Expando objects
=================

Altered States also contains an optional feature called `Expando`
objects. It's a simple object that can be used to create replacement
structures easily. It's basically an empty object that you can add any
extra attributes to, with a conceptual implementation along the lines
of::

   class Expando(object):
       def __init__(self, *args, **kw):
           self.__dict__.update(kw)

Full source is marginally more complex, see `here
<https://github.com/Plexical/altered.states/blob/master/altered/base.py#L1>`_. So
if you need an object with another object embedded that has a method
you can create that with::

    >>> from altered import Expando
    >>> faked_ctx = Expando(user=Expando(get_name=lambda: 'Foo Bar'))
    >>> faked_ctx.user.get_name()
    'Foo Bar'

Using and `Expando` object with Altered States can look like this::

    >>> from altered import Expando, state
    >>> obj = Expando(a=1)
    >>> @state(obj, a=3)
    ... def fn():
    ...     return obj.a
    >>> fn()
    3

`Expando` classes are aliased to the name `E` if you're seeking
maximum terseness.
