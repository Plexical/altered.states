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
