#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from firebase import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()


setup(name='python-firebase',
      version=__version__,
      description="Python interface to the Firebase's REST API.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Natural Language :: English',
      ],
      keywords='firebase python',
      author='Ozgur Vatansever',
      author_email='ozgurvt@gmail.com',
      maintainer='Ozgur Vatansever',
      maintainer_email='ozgurvt@gmail.com',
      url='http://ozgur.github.com/python-firebase/',
      license='MIT',
      packages=['firebase'],
      test_suite='tests.all_tests',
      install_requires=['requests>=1.1.0'],
      zip_safe=False,
)
