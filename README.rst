======================================================================
Kittypack: A silly little tool to poke archlinux.org/packages for info
======================================================================
:Author: Øyvind 'Mr.Elendig' Heggstad

Description
===========

| This is a -program- written by Mr.Elendig.
| It menaces with spikes of crud and is decorated with hanging rings of fail.
| On the program is a picture of bugs in python.

Dependencies
============
| python 3.x
| python-requests
| python-docopt
| python-yaml
| python-curtsies

Instalation
============
| python3 setup.py install
| or better, use your distributions build system

Usage
=====

kittypack [options] <pkg>

Options:
  -r, --repository=<repo>     Search only in <repo>
  -a, --architecture=<arch>   Search only in <arch>
  -j, --json                  Print the raw json
  -h, --help                  Show this screen
  -c, --config=<config>       Path to the config [default: /etc/kittypack.conf]
