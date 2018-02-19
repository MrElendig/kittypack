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

# Various formaters etc for kittypack
import curtsies
import re

def template_output(pkg):
    """ Creates a output string from a package
    :parmans pkg: dict like object describing a package
    :returns string
    """
    template = ("{repo}/{arch}/{pkgname}  {epoch}:{pkgver}-{pkgrel}{ood}\n"
                "  Updated: {last_update}  Built: {build_date}")
    data = {}
    data["repo"] = curtsies.fmtstr(pkg["repo"], fg="magenta", bold=True)
    data["arch"] = curtsies.fmtstr(pkg["arch"], fg="yellow", bold=True)
    data["pkgname"] = curtsies.fmtstr(pkg["pkgname"], fg="green", bold=True)
    if pkg["flag_date"]:
        ver_colour = "red"
        data["ood"] = curtsies.fmtstr(" <!>", fg=ver_colour)
    else:
        ver_colour = "green"
        data["ood"] = ""
    for itm in ("epoch", "pkgver", "pkgrel"):
        # fmtstr doesn't like ints
        data[itm] = curtsies.fmtstr(str(pkg[itm]), fg=ver_colour, bold=True)
    data["last_update"] = pkg["last_update"]
    data["build_date"] = pkg["build_date"]
    return template.format(**data)


def format_output(fstring, pkg):
    """ Creates a output string from a format string naively
    :params fstring: format string
    :parmans pkg: dict like object describing a package
    :returns string
    """
    lookup = {
            "%a": "arch",
            "%B": "build_date",
            "%b": "pkgbase",
            "%C": "compressed_size",
            "%c": "conflicts",
            "%D": "depends",
            "%d": "pkgdesc",
            "%e": "epoch",
            "%f": "filename",
            "%f": "flag_date",
            "%g": "groups",
            "%I": "installed_size",
            "%L": "licenses",
            "%l": "pkgrel",
            "%M": "maintainers",
            "%n": "pkgname",
            "%p": "packager",
            "%P": "provides",
            "%R": "replaces",
            "%r": "repo",
            "%U": "last_updated",
            "%u": "url",
            "%v": "pkgver",
            }

    tokens = set(re.findall('(%.)', fstring))
    for token in tokens:
        if token == "%%":
            fstring = re.sub("%%", "%", fstring)
        else:
            fstring = re.sub(token, str(pkg[lookup[token]]), fstring)
    return fstring

