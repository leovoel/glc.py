from setuptools import setup, find_packages
from glc import __version__

import os


required = []
with open("requirements.txt") as f:
    required = f.read().splitlines()


with open("README.md") as f:
    readme = f.read()

setup(
    name="glc.py",
    author="leovoel",
    url="https://github.com/leovoel/glc.py",
    version=__version__,
    license="MIT",
    description="Python library for the creation of code-based animations.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Graphics"
    ]
)
