from setuptools import setup, find_packages

# read the contents of the README file for PyPI
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name="asciigit",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.2",
    packages=find_packages(),
    tests_require=['mock'],
    install_requires=[
        'asciimatics',
        'GitPython',
        'pydriller'
    ],
    entry_points={
        "console_scripts": [
            "asciigit = src.main:main",
        ],
    }
)
