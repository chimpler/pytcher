#!/usr/bin/env python

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


setup(
    name='pytcher',
    version='0.0.1',
    description='Micro framework for Python',
    long_description='Micro framework for Python',
    keywords='hocon parser',
    license='Apache License 2.0',
    author='Francois Dang Ngoc',
    author_email='francois.dangngoc@gmail.com',
    url='http://github.com/chimpler/pytcher',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[
        'pytcher',
    ],
    install_requires=[],
    tests_require=['pytest', 'mock'],
    test_suite='tests'
)
