===================================
 Python monkey-patching for Humans
===================================

*Altered States* tries to take the concept of `Python for Humans
<http://python-for-humans.heroku.com/>`_ to the world of `monkey
patching <http://en.wikipedia.org/wiki/Monkey_patch>`_. A `search
<http://pypi.python.org/pypi?%3Aaction=search&term=monkey+patch>`_ On
PyPI shows that there are already many often technically sophisticated
packages that does this. The thing with them is that they are all
making a procedure that should be relatively simple complicated.

With Altered States you get to choose between two functions, one that
can either manipulate your world via a **with** statement::

    >>> from altered import state
    >>> class Anon(object): pass
    >>> o = Anon()
    >>> o.foo = 'foo'
    >>> with state(o, foo='bar'):
    ...     print(o.foo)
    bar

or using a **decorator**::

    >>> from altered import state
    >>> struct = {'a': 1}
    >>> @state(struct, a=3)
    ... def fn():
    ...     return struct['a']
    >>> fn()
    3

This example also shows how **.state()** can be applied to **dict**'s
as well as objects.

From version `0.8.5`, you can also make changes in two steps (e.g. if
you need setup/teardown steps in a test) using the
**.alter()** function::

    >>> from altered import alter, E
    >>> o = E(foo='foo')
    >>> restore = alter(o, foo='bar')
    >>> print(o.foo)
    bar
    >>> restore()
    >>> print(o.foo)
    foo

Just like **.state()**, **.alter()** works on **dict**'s too::

    >>> from altered import alter
    >>> struct = {'a': 1}
    >>> restore = alter(struct, a=3)
    >>> print(struct)
    {'a': 3}
    >>> restore()
    >>> print(struct)
    {'a': 1}

**.alter()** can of course not keep track of downstream Exceptions
like **.state()** can, so if you need to guarantee state restoration,
it's up to you to ensure that the returned restoration function is
actually called.

Altered States runs on Python 2.7 and 3.5+.

Purpose
-------

I implemented the code that later became Altered States beacuse I was
unhappy about how fixture setup was obscuring actual test code in test
suites, and that is also the recommended primary use of Altered
States. But there are other usecases where a reversible change of the
environment can be useful (switching between authenticated users,
temporary I/O redirection, probably more).

Expando objects
---------------

Altered States also contains an optional feature called **Expando**
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

If we revisit the second example, it can be expressed with an
**Expando** object like this::

    >>> from altered import Expando, state
    >>> obj = Expando(a=1)
    >>> @state(obj, a=3)
    ... def fn():
    ...     return obj.a
    >>> fn()
    3

**Expando** is also aliased to the shorter name **E** for terser
nesting::

   >>> from altered import E
   >>> fakey = E(substruct=E(membr='foo', method=lambda: 'x'))

Reference documentation
-----------------------

More detailed (but incomplete as of yet) documentation can be found at
Read The Docs `here <http://altered-states.rtfd.org>`_.

What was the name again?
------------------------

You mean you haven't seen the `movie
<http://www.imdb.com/title/tt0080360/>`_? Go see it, it's a trip! And
when you see it, take note of the implicit warning in the film of what
happens if you take your usage too far:

*The whole* **idea** *of Altered States is to create
side-effects. Please use Altered States responsibly.*
