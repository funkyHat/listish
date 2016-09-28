# pylint:disable=missing-docstring

from setuptools import setup

import listish


setup(
    name='listish',
    version=listish.__version__,
    description=listish.__doc__,
    author='Matt Wheeler, Connor Shearwood',
    author_email='m@funkyhat.org',
    url='https://github.com/funkyHat/listish',
    py_modules=['listish'],
    license='Apache 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
