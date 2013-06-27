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

@state(vars(), injected='foo')
def test_patch_inplace():
    assert injected == 'foo'

def test_os_environ():
    with state(os.environ, ALTERED='states'):
        assert os.environ['ALTERED'] == 'states'

    assert 'ALTERED' not in os.environ

def test_decorator_os_environ():
    @state(os.environ, ALTERED='states')
    def check():
        return os.environ['ALTERED']

    assert check() == 'states'
    assert 'ALTERED' not in os.environ

@pytest.fixture
def w_getitem():
    class implements_getitem(object):
        def __getitem__(self, key):
            return 'foo'
    return implements_getitem()

def test_getitem_overridable(w_getitem):
    with state(w_getitem, any='changed'):
        assert w_getitem.any == 'changed'
