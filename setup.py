#!/usr/bin/env python3

import distutils.core

distutils.core.setup(
    name='kittypack',
    version='0.2',
    description='A silly little tool to get info from archlinux.org/packages',
    author="Øyvind 'Mr.Elendig' Heggstad",
    author_email='mrelendig@har-ikkje.net',
    url='https://github.com/MrElendig/kittypack',
    scripts=['bin/kittypack'],
    data_files=[('/etc/', ['conf/kittypack.conf'])]
)
