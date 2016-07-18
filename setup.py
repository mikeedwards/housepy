#!/usr/bin/env python

from distutils.core import setup

setup(
    name='housepy',
    version='0.0.1',
    description='Personal utility library for Python 3',
    author='Brian House',
    url='https://github.com/brianhouse/housepy',
    py_modules=['housepy'],
    package_dir={'housepy': ''},
    packages=['housepy'],
    install_requires=[
        'beautifulsoup4>=4.4.1',
        'boto>=2.39.0',
        'cairocffi>=0.7.2',
        'cffi>=1.5.2',
        'cycler>=0.10.0',
        'Jinja2>=2.8',
        'Markdown>=2.6.6',
        'MarkupSafe>=0.23',
        'matplotlib>=1.5.1',
        'numpy>=1.11.0',
        'Pillow>=3.1.1',
        'PyAudio>=0.2.9',
        'pycrypto>=2.6.1',
        'pyglet>=1.2.4',
        'pymongo>=3.2.2',
        'pyparsing>=2.1.1',
        'pyserial>=3.0.1',
        'python-dateutil>=2.5.2',
        'python-geohash>=0.8.5',
        'python-rtmidi==0.5b1',
        'pytz>=2016.3',
        'PyYAML>=3.11',
        'requests>=2.9.1',
        'scipy>=0.17.0',
        'six>=1.10.0',
        'tinys3>=0.1.11',
        'tornado>=4.3',
    ],
)
