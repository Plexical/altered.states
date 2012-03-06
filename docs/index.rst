Altered States: Python monkey-patching for Humans
=================================================

Altered States is a way to simplify `monkey patching
<http://en.wikipedia.org/wiki/Monkey_patch>`_ and make it more
accessible. It was written with test fixture setup in mind but can be
used for anything that needs a reversible and temporary drastic state
change (switching between authenticated users, I/O redirection,
probably more).

You use Altered State by calling just *one* function, :py:func:`state`.

Either via a context manager (`with` statement)::

    >>> from altered import state
    >>> class Anon(object): pass
    >>> o = Anon()
    >>> o.foo = 'foo'
    >>> with(state(o, foo='bar')):
    ...     print o.foo
    bar

or using the same function as a a `decorator`::

    >>> from altered import state
    >>> struct = {'a': 1}
    >>> @state(struct, a=3)
    ... def fn():
    ...     return struct['a']
    >>> fn()
    3

This example also shows how :py:func:`state` can be applied to `dict` as
well as objects.

Contents:

.. toctree::
   :maxdepth: 2

   examples
   expando
   state-ref
   forget


More
====

* :ref:`search`

