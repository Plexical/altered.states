Python monkey-patching for Humans
===================================

*Altered States* tries to take
[@kennethreitz](https://github.com/kennethreitz) concept of [Python
for Humans](http://python-for-humans.heroku.com/) and applies it to
[monkey patching](http://en.wikipedia.org/wiki/Monkey_patch). A
[search](http://pypi.python.org/pypi?%3Aaction=search&term=monkey+patch)
on PyPI shows that there are already many often technically
sophisticated packages that does this. The thing with them is that
they are all making a procedure that should be relatively simple quite
complicated.

Altered States tries to keep the API maximally simple. Either
manipulate your world via the `with` statement:

```python
>>> from altered import Expando, state
>>> obj = Expando(a=1)
>>> with(state(obj, a=2)):
...     print obj.a
2
```

or using a `decorator`:

```python
>>> from altered import Expando, state
>>> obj = Expando(a=1)
>>> @state(obj, a=3)
>>> def fn():
...     return obj.a
>>> fn()
3
```

Altered States is known to run on Python 2.5, 2.6 and 27. Python 3+
support should follow shortly.
