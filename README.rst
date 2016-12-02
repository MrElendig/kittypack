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
| python-setuptools

Instalation
============
| pip --user install .
| or better, use your distributions build system

Usage
=====

kittypack [options] <pkg>

Options:
  -r, --repository=<repo>     Search only in <repo>
  -a, --architecture=<arch>   Search only in <arch>
  -f, --format=<fstring>      Use custom format string
  -j, --json                  Print the raw json
  -c, --config=<config>       Path to the config [default: /etc/kittypack.conf]
  -h, --help                  Show this screen

The output format supports the following tokens::

 %%     literal %
 %a     arch
 %B     build_date
 %b     pkgbase
 %C     compressed_size
 %c     conflicts
 %D     depends
 %d     pkgdesc
 %e     epoch
 %f     filename
 %f     flag_date
 %g     groups
 %I     installed_size
 %L     licenses
 %l     pkgrel
 %M     mainainers
 %n     pkgname
 %p     packager
 %P     provides
 %R     replaces
 %r     repo
 %U     last_updated
 %u     url
 %v     pkgver
