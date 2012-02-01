===================================
 Python monkey-patching for Humans
===================================

*Altered States* tries to take @kennethreitz concept of `Python for
Humans`_ and applies it to `monkey patching`_. A search_ on PyPI shows
that there are already many often technically sophisticated packages
that does this. The thing with them is that they are all making a
procedure that should be relatively simple quite complicated.

.. _Python for Humans: http://python-for-humans.heroku.com/
.. _monkey patching: http://en.wikipedia.org/wiki/Monkey_patch
.. _search: http://pypi.python.org/pypi?%3Aaction=search&term=monkey+patch

Altered States tries to keep the API maximally simple. Either
manipulate your world via the `with` statement:

>>> from altered import Expando, state
>>> obj = Expando(a=1)
>>> with(state(obj, a=2)):
...     print obj.a
2

or using a `decorator`:

>>> import altered
>>> obj = altered.Expando(a=1)
>>> @altered.decostate(obj, a=3)
>>> def fn():
...     return obj.a
>>> fn()
3
