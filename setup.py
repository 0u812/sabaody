#! /usr/bin/env python

from setuptools import setup

setup(name='sabaody',
      version='0.1.0',
      description='Distributed Island Model',
      author='Shaik Asifullah, J. Kyle Medley',
      packages=['sabaody'],
      install_requires=[
        'tellurium',
        'networkx>=2.1',
        'pymemcache>=1.4.4',
        'toolz>=0.9.0',
        'marshmallow=>2.15.2',
        'arrow>=0.12.1',
        'tornado>=5.0.2',
        'APScheduler>=3.5.1',
        'requests>=2.18.0',
        'yarl>=1.2.4',
        'attrs>=18.1.0',
        ],
      )
