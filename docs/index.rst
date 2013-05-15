Altered States: Python monkey-patching for Humans
=================================================

Altered States is a way to simplify `monkey patching
<http://en.wikipedia.org/wiki/Monkey_patch>`_ and make it more
accessible. It was written with test fixture setup in mind but can be
used for anything that needs a reversible and temporary drastic state
change (switching between authenticated users, I/O redirection,
probably more).

API
---

There are two ways to manipulate your world.

state
+++++

For quick state changes, use the :py:func:`state` function by way of a
context manager (`with` statement)::

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

alter/restore
+++++++++++++

*(This feature is available from version `0.8.5`)*.

If you need the state to be in effect for a bit longer, use the
two-step procedure by calling :py:func:`alter`. It returns another
function that will perform the restoration at a later time::

    >>> from altered import alter, E
    >>> o = E(foo='foo')
    >>> restore = alter(o, foo='bar')
    >>> print(o.foo)
    bar
    >>> restore()
    >>> print(o.foo)
    foo

It also takes `dict` -like objects in the same way that
:py:func:`state` does.

Contents:

.. toctree::
   :maxdepth: 2

   examples
   expando
   state-ref
   alter-ref
   forget


More
====

* :ref:`search`

