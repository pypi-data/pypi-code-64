# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.2'


setup(
    name='pyfs-application',
    version=version,
    keywords='Feishu Application',
    description='Feishu Application Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/feishu-sdk-python/pyfs-application.git',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pyfs_application'],
    py_modules=[],
    install_requires=['pyfs-auth>=1.0.3'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
