# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='darshak',
      version='0.1.0',
      description='darshak for pdf viewer',
      long_description=readme,
      author='Kenneth Reitz',
      author_email='',
      url='https://github.com/srbhp/darshak',
      license=license,
      packages=find_packages(exclude=('tests', 'docs')))
