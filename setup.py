#!/usr/bin/env python3
from setuptools import setup, find_packages
from distutils.util import convert_path
import os

__author__ = 'adamkoziol'
__author__ = 'LargeKowalski888'
__author__ = 'noorshu'

# Find the version
version = {}
with open(convert_path(os.path.join('hashr', 'version.py')), 'r', encoding='utf-8') as version_file:
    exec(version_file.read(), version)

setup(
    name="MiseqHashR",
    version=version['__version__'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'MiseqHashR = hashr.miseq_hashr:cli'
        ],
    },
    include_package_data=True,
    author="Adam Koziol",
    author_email="adam.koziol@inspection.gc.ca",
    url="https://github.com/OLC-LOC-Bioinformatics/MiSeqHashR",
)
