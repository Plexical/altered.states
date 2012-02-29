===================================
 Python monkey-patching for Humans
===================================

*Altered States* tries to take the concept of `Python for Humans
<http://python-for-humans.heroku.com/>`_ to the world of `monkey
patching <http://en.wikipedia.org/wiki/Monkey_patch>`_. A `search
<http://pypi.python.org/pypi?%3Aaction=search&term=monkey+patch>`_ on
PyPI shows that there are already many often technically sophisticated
packages that does this. The thing with them is that they are all
making a procedure that should be relatively simple complicated.

With Altered States you only call *one* function, **altered.state()**.
Manipulate your world via the **with** statement::

    >>> import sys
    >>> from StringIO import StringIO
    >>> from altered import state
    >>> buf = StringIO()
    >>> with(state(sys, stdout=buf)):
    ...     print 'foo'
    >>> buf.getvalue()
    'foo\n'

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

Altered States has been verified to run on Python 2.5, 2.6 and 27.

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
