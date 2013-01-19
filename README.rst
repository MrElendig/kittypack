======================================================================
Kittypack: A silly little tool to poke archlinux.org/packages for info
======================================================================
:Author: Øyvind 'Mr.Elendig' Heggstad

Description
===========

| This is a -program- written by Mr.Elendig.
| It menaces with spikes of crud and is decorated with hanging rings of fail.
| On the program is a picture of bugs in python.

Innstalation
============
| cp kittypack.py some/where/in/$PATH/kittypack  # chmod/chown as needed
| cp kittypack.conf /etc/kittypack.conf  # or just use the -c flag

Usage
=====

kittypack [options] <pkg>

Options:
  -r, --repository=<repo>     Search only in <repo>
  -a, --architecture=<arch>   Search only in <arch>
  -j, --json                  Print the raw json
  -h, --help                  Show this screen
  -c, --config=<config>       Path to the config [default: /etc/kittypack.conf]
