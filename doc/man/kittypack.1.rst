=========
kittypack
=========

-------------------------------------------------------------
A tool to grab basic package info from archlinux.org/packages
-------------------------------------------------------------

:Author: Øyvind Heggstad <mrelendig@har-ikkje.net>
:Date: 2014-03-21
:Copyright: AGPLv3
:Version: 0.1
:Manual section: 1
:Manual group: None

SYNOPSIS
========

kittypack [options] <pkg>

DESCRIPTION
===========

This is a -program- written by Mr.Elendig.
It menaces with spikes of crud and is decorated with hanging rings of fail.
On the program is a picture of bugs in python.

OPTIONS
=======

-r, --repository=<repo>     Search only in <repo>
-a, --architecture=<arch>   Search only in <arch>
-f, --format=<fstring>      Use custom format string
-j, --json                  Print the raw json
-c, --config=<config>       Path to the config [default: /etc/kittypack.conf]
-h, --help                  Show the help screen

FORMATTING
==========

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
 %M     maintainers
 %n     pkgname
 %p     packager
 %P     provides
 %R     replaces
 %r     repo
 %U     last_updated
 %u     url
 %v     pkgver

BUGS
====

Everything
