#!/usr/bin/env python3

# kittypack: Grabs package info off archlinux.org/packages
# Copyright (C) 2012  Øyvind 'Mr.Elendig' Heggstad

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

setup(
    name="kittypack",
    version="0.2.1",
    description="A silly little tool to get info from archlinux.org/packages",
    url="https://github.com/MrElendig/kittypack",
    author="Øyvind \"Mr.Elendig\" Heggstad",
    author_email="mrelendig@har-ikkje.net",
    license="AGPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.5",
        "Environment :: Console"
    ],

    keywords="sample setuptools development",
    packages=["kittypack"],
    install_requires=["docopt", "requests", "pyyaml", "curtsies",
        "setuptools"],
    package_data={
        "kittypack": ["kittypack.conf"],
    },
    entry_points={
        "console_scripts": [
            "kittypack=kittypack.app:main",
        ],
    },
)
