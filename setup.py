#!/usr/bin/env python
# coding: utf8

from setuptools import setup, find_packages
from setuptools.command.test import test

# avoid importing the module 
exec(open('projectmanager/_version.py').read())

setup(
    name='django-projectmanager',
    version=__version__,
    description='Time tracking, task management and invoicing for ' +
                'individuals or small teams.',
    long_description=open('readme.md').read(),
    author='Greg Brown',
    author_email='greg@gregbrown.co.nz',
    url='https://github.com/gregplaysguitar/django-projectmanager',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['Django>=1.8', 'xhtml2pdf>=0.0.6', 'Jinja2>=2.7.3'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
)
