from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='python-firebase',
      version=version,
      description="Python library for the Firebase Real-Time Web Backend",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='firebase python',
      author='Ozgur Vatansever',
      author_email='ozgurvt@gmail.com',
      url='',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
