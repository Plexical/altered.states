==========
 Examples
==========

Here are some examples to get you started on usage of Altered States:

I/O redirection
---------------

    >>> import sys
    >>> from StringIO import StringIO
    >>> from altered import state
    >>> buf = StringIO()
    >>> with(state(sys, stdout=buf)):
    ...     print 'foo'
    >>> buf.getvalue()
    'foo\n'

Faking an import
----------------

    >>> import sys
    >>> from altered import state, Expando
    >>> with(state(sys.modules, fakey=Expando(foo='bar') )):
    ...     import fakey
    ...     print fakey.foo
    bar

In-place patching
-----------------

    >>> @state(globals(), injected='foo')
    ... def fn():
    ...     return injected
    >>> fn()
    'foo'
