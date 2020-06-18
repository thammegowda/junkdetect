#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/12/20


import junkdetect
from pathlib import Path

from setuptools import setup, find_packages

long_description = Path('README.md').read_text(encoding='utf-8', errors='ignore')

classifiers = [  # copied from https://pypi.org/classifiers/
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Text Processing',
    'Topic :: Utilities',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Filters',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
]

setup(
    name='junkdetect',
    version=junkdetect.__version__,
    description=junkdetect.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache Software License 2.0',
    classifiers=classifiers,
    python_requires='>=3.6',
    url='https://github.com/thammegowda/junkdetect',
    download_url='https://github.com/thammegowda/junkdetect',
    platforms=['any'],
    author='Thamme Gowda',
    author_email='tgowdan@gmail.com',
    packages=find_packages(),  # for a single .py file, use py_modules=[]
    entry_points={
        'console_scripts': ['junkdetect=junkdetect:perplex.main'],
    },
    install_requires = ['requests', 'sentencepiece', 'torch >= 1.3', 'regex', 'tqdm']
)
