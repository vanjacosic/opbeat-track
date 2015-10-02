# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('opbeat_track/opbeat_track.py').read(),
    re.M
).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="opbeat-track",
    packages=["opbeat_track"],
    entry_points={
        "console_scripts": ['opbeat-track = opbeat_track.opbeat_track:main']
    },
    version=version,
    description="Small dependency-free CLI tool to track releases to Opbeat",
    long_description=long_descr,
    author="Vanja Cosic",
    author_email="vanja@opbeat.com",
    url="https://github.com/vanjacosic/opbeat-track",
)
