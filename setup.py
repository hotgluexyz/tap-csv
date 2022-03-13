#!/usr/bin/env python

from setuptools import setup

setup(name='tap-csv',
      version='0.1.2',
      description='Singer.io tap for extracting data from a CSV file',
      author='Robert J. Moore',
      url='http://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_csv'],
      install_requires=[
          'singer-python==5.7.0',
          'backoff==1.8.0',
          'requests==2.12.4',
      ],
      entry_points='''
          [console_scripts]
          tap-csv=tap_csv:main
      ''',
      packages=['tap_csv'],
      package_data = {
          'tap_csv/schemas': [
          ],
      },
      include_package_data=True,
)

