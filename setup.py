#!/usr/bin/env python
from setuptools import setup, find_packages


# Parse version number from livingthings/__init__.py:
with open('livingthings/__init__.py') as f:
    info = {}
    for line in f.readlines():
        if line.startswith('version'):
            exec(line, info)
            break


setup_info = dict(
    name='livingthings',
    version=info['version'],
    author='Ryoji Kuwae Neto',
    author_email='ryojikn@gmail.com',
    url='http://livingthings.readthedocs.org/en/latest/',
    download_url='http://pypi.python.org/pypi/livingthings',
    project_urls={
        'Documentation': 'https://livingthings.readthedocs.io/en/latest',
        'Source': 'https://github.com/ryojikn/livingthings',
        'Tracker': 'https://github.com/ryojikn/livingthings/issues',
    },
    description='Raspberry-pi based robotics library for enabling specific behaviors',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=[
        'Development Status :: 1 - Development',
        'Environment :: Raspberry pi 4',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Robotics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=['livingthings'] + ['livingthings.' + pkg for pkg in find_packages('livingthings')],

    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,
)

setup(**setup_info)