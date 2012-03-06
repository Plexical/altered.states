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

Deny the existance of a module
------------------------------

*It'd be much better if it would raise `ImportError` here. Maybee later.*

    >>> import sys
    >>> from altered import state, forget
    >>> with(state(sys.modules, shutil=forget)):
    ...     import shutil
    Traceback (most recent call last):
    KeyError: 'shutil'
    >>> import shutil

Nested structure
----------------

    >>> from altered import state, Expando
    >>> ctx = Expando()
    >>> idx = 0
    >>> users = [Expando(name='Foo', get_token=lambda: 'xyz')]
    >>> @state(ctx, users=users)
    ... def token(idx):
    ...     return ctx.users[idx].get_token()
    >>> token(0)
    'xyz'
