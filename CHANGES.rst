1.0.1
-----

* Fixed issue in setup.py script
* Added missing changelog

1.0.0
-----

* Altered States now runs on Python 3 (tested on 2.7, 3.5 and 3.6)
* Dropped support for Python 2.6
* Experimental support for Kenneth Reitz Pipenv tool
* Corrected invalid use of `os.modules` in examples
* Altered States is now coveraged by `coverage.py`

0.8.6
-----

* Better handling of objects that override `__getitem__` (thanks to
  @merwok).
* Drop support for Python 2.5 (no sane way to solve issue #4 there).

0.8.5
-----

* Added a new API entry point: `alter()`, that can be used to perform
  a two-step reversible alteration.

0.8.2
-----

* Updated test suites to use `@pytest.fixture` notation for fixtures
  (now requires `py.test` > 2.3)
* Fixes a bug causing `os.environ` not to be patchable.

Fixing bug #2 means switching the `dict` -like object check from
`isinstance(x, dict)` to `hasattr(x, '__getitem__')`. This change is
thought to not break backwards compatibility but if you encounter
unexpected behaviour in `dict` / `object` detection this might be
it. I'd be very interested to know about that if you do.

0.8.1
-----

* Alias `Expando` as `E` for optional terseness.

0.8.0
-----

Initial release.
