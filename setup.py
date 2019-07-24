import sys
from setuptools import setup, find_packages

setup (
    name="asciigit",
    version="0.0.1",
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
