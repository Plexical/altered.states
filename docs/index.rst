Altered States: Python monkey-patching for Humans
=================================================

Altered States is a way to simplify `monkey patching
<http://en.wikipedia.org/wiki/Monkey_patch>`_ and make it more
accessible. It was written with test fixture setup in mind but can be
used for anything that needs a reversible and temporary drastic state
change (switching between authenticated users, I/O redirection,
probably more).

You use Altered State by calling just *one* function, `altered.state()`.

Either via a context manager (`with` statement)::

    >>> import sys
    >>> from StringIO import StringIO
    >>> from altered import state
    >>> buf = StringIO()
    >>> with(state(sys, stdout=buf)):
    ...     print 'foo'
    >>> buf.getvalue()
    'foo\n'

or using the same function as a a `decorator`::

    >>> from altered import state
    >>> struct = {'a': 1}
    >>> @state(struct, a=3)
    ... def fn():
    ...     return struct['a']
    >>> fn()
    3

This example also shows how **.state()** can be applied to **dict**'s
as well as objects.

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

