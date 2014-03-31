#!/usr/bin/env python

from setuptools import setup

setup(name='Generic Celery task',
      version='0.1',
      description='A workaround for the lack of dynamic tasks in Celery',
      long_description=open("README.rst").read(),
      author='Stefan Talpalaru',
      author_email='stefantalpalaru@yahoo.com',
      url='https://github.com/stefantalpalaru/generic_celery_task',
      license = 'BSD',
      packages=['generic_celery_task'],
      test_suite = 'nose.collector',
      install_requires=['celery'],
      tests_require=['nose', 'redis'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: BSD License',
          'Topic :: System :: Distributed Computing',
          'Topic :: Software Development :: Object Brokering',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: POSIX',
      ],
     )

