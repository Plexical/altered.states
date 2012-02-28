Altered States: humane monkey patching for Python
=================================================

Altered States is a way to simplify `monkey patching
<http://en.wikipedia.org/wiki/Monkey_patch>`_ and make it more
accessible. It was written with test fixture setup in mind but can be
used for anything that needs a reversible and temporary drastic state
change (switching between authenticated users, I/O redirection,
probably more).

You use Altered State by calling just *one* function, `altered.state()`.

Either via a context manager (`with` statement):

::

    >>> from altered import Expando, state
    >>> obj = Expando(a=1)
    >>> with(state(obj, a=2)):
    ...     print obj.a
    2

or using the same function as a a `decorator`:

::

    >>> from altered import Expando, state
    >>> obj = Expando(a=1)
    >>> @state(obj, a=3)
    >>> def fn():
    ...     return obj.a
    >>> fn()
    3


Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

