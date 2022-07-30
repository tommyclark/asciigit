from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="asciigit",
    description="A command line ASCII Git GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tommyclark/asciigit",
    version="0.0.16",
    packages=find_packages(),
    tests_require=["mock"],
    install_requires=["asciimatics>=1.14.0", "GitPython>=3.1.20", "pydriller>=2.1"],
    entry_points={
        "console_scripts": [
            "asciigit = src.main:main",
        ],
    },
)
