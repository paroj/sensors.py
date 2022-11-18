#!/usr/bin/env python

from distutils.core import setup

setup(name='sensors.py',
      version='2.0',
      description='Python bindings for libsensors3',
      author='Pavel Rojtberg',
      url='https://github.com/paroj/sensors.py',
      py_modules=['sensors'],
      license='LGPLv2',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
)