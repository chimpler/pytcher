#!/usr/bin/env python

import sys
from setuptools import setup
import subprocess
from setuptools.command.install import install
from setuptools.command.develop import develop
from datetime import datetime


class CustomInstallCommand(install):
    def run(self):
        create_version_file()
        self.do_egg_install()


class CustomDevelopCommand(develop):
    def run(self):
        create_version_file()
        super(CustomDevelopCommand, self).run()


def create_version_file():
    app_version = subprocess.Popen(sys.argv[0] + " --version", shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode()
    commit_hash = subprocess.Popen("git rev-parse HEAD", shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode()

    with open('pytcher/_version.py', 'wt') as fd:
            fd.write("git_version = '%s'\n" % commit_hash)
            fd.write("app_version = '%s'\n" % app_version)
            fd.write("built_at = '%s'\n" % datetime.now())


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
    install_requires=[
    ],
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand
    }
)
