import sys
from setuptools import setup, find_packages

setup (
    name = "asciigit",        # what you want to call the archive/egg
    version = "0.1",
    packages=find_packages(),
    tests_require=['mock'],
    install_requires=[
        'asciimatics',
        'GitPython',
        'pydriller'
    ],
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "asciigit = src.main:main",
        ],
    }
)
