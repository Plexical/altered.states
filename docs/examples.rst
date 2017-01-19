==========
 Examples
==========

Here are some examples to get you started on usage of Altered States:

I/O redirection
---------------

    >>> import sys
    >>> from altered import state, py23compat
    >>> buf = py23compat.strio()
    >>> with state(sys, stdout=buf):
    ...     print('foo')
    >>> buf.getvalue()
    'foo\n'

Faking an import
----------------

    >>> import sys
    >>> from altered import state, Expando
    >>> with state(sys.modules, fakey=Expando(foo='bar') ):
    ...     import fakey
    ...     print(fakey.foo)
    bar

In-place patching
-----------------

Module scope
~~~~~~~~~~~~

    >>> @state(globals(), injected='foo')
    ... def fn():
    ...     return injected
    >>> fn()
    'foo'

Local scope
~~~~~~~~~~~

    >>> from altered import state, E
    >>> with state(vars(), injected='foo'):
    ...    print(injected)
    foo

Deny the existance of a module
------------------------------

    >>> import sys
    >>> from altered import state
    >>> with state(sys.modules, shutil=None):
    ...     import shutil # doctest: +SKIP
    Traceback (most recent call last):
        ...
    ModuleNotFoundError: import of 'shutil' halted; None in sys.modules
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
