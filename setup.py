#!/usr/bin/env python

from setuptools import setup

setup(
    name='tap-csv',
    version='1.0.0',
    description='Singer.io tap for extracting data from a CSV/XLSX file',
    author='hotglue',
    url='http://singer.io',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_csv'],
    entry_points='''
        [console_scripts]
        tap-csv=tap_csv:main
    ''',
    packages=['tap_csv']
)
