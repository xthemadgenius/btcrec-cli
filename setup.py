#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="btcrecover-cli",
    version="1.0.0",
    author="3rdIteration",
    author_email="",
    description="Bitcoin wallet password and seed recovery tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3rdIteration/btcrecover",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "btcrecover=btcrecover_cli.main:main",
            "btcrecover.py=btcrecover_cli.btcrecover:main",
            "seedrecover.py=btcrecover_cli.seedrecover:main",
            "seedrecover_batch.py=btcrecover_cli.seedrecover_batch:main",
            "create-address-db.py=btcrecover_cli.create_address_db:main",
            "check-address-db.py=btcrecover_cli.check_address_db:main",
        ],
    },
    include_package_data=True,
    package_data={
        "btcrecover": [
            "wordlists/*.txt",
            "opencl/*.cl",
        ],
    },
    zip_safe=False,
)