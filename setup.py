#!/usr/bin/env python

from altered import meta

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=meta.name,
    version=meta.version,
    description='Python monkey patching for humans.',
    long_description=open('README.rst').read(),
    packages=('altered',),
    url=meta.url,
    author=meta.author,
    author_email=meta.author_email,
    license='ISC',
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
    ),
)
