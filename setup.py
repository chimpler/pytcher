#!/usr/bin/env python

import subprocess
import sys
from datetime import datetime

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.test import test


class CustomTestCommand(test):
    def run(self):
        create_version_file()
        super(CustomTestCommand, self).run()


class CustomInstallCommand(install):
    def run(self):
        create_version_file()
        self.do_egg_install()


class CustomDevelopCommand(develop):
    def run(self):
        create_version_file()
        super(CustomDevelopCommand, self).run()


def create_version_file():
    app_version = subprocess.Popen(sys.argv[0] + " --version", shell=True,
                                   stdout=subprocess.PIPE).stdout.read().strip().decode()
    commit_hash = subprocess.Popen("git rev-parse HEAD", shell=True,
                                   stdout=subprocess.PIPE).stdout.read().strip().decode()

    with open('pytcher/_version.py', 'wt') as fd:
        fd.write("git_version = '%s'\n" % commit_hash)
        fd.write("app_version = '%s'\n" % app_version)
        fd.write("built_at = '%s'\n" % datetime.now())


setup(
    name='pytcher',
    version='0.0.2',
    description='Micro framework for Python',
    long_description='Micro framework for Python',
    keywords='python rest routing framework',
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
    install_requires=[
        'python-dateutil',
        'pytz',
        'watchdog'
    ],
    packages=[
        'pytcher',
    ],
    extras_require={
        'json-path': [
            'jsonpath-ng'
        ],
        'mkdocs': [
            'mkdocs-material',
            'markdown-include'
        ]
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'test': CustomTestCommand
    }
)
