"""
This isn't a test suite in the traditional sense (testing
correctness), rather a test suite to verify assumptions I make about
how Altered States should behave in a "realistic" environment.
"""
from __future__ import with_statement
import sys
import os
import subprocess

import pytest

from StringIO import StringIO

from altered import state, Expando

def test_capture_stdout():
    buf = StringIO()
    print('Foo')
    with(state(sys, stdout=buf)):
        print('Bar')
    assert buf.getvalue() == 'Bar' + os.linesep

# Bit of a pain to set up, but sometime:
# @state(os.environ, DJANGO_SETTINGS_MODULE='proj.settings')
# def test_django_case():
#     from proj import models
#     stuff = models.Model.objects.filter(... # you get the idea

def test_patch_sys_modules():
    with(state(sys.modules, fakey=Expando(foo='bar'))):
        import fakey
        assert fakey.foo == 'bar'
    with(pytest.raises(ImportError)):
        import fakey

@state(globals(), injected='foo')
def test_patch_module():
    assert injected == 'foo'
