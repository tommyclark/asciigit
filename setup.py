from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup (
    name="asciigit",
    description="A command line ASCII Git GUI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/tommyclark/asciigit",
    version="0.0.7",
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
