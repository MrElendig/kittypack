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

"""kittypack: A tool to grab basic package info from archlinux.org/packages

Usage:  kittypack [options] <pkg>

Options:
  -r, --repository=<repo>     Search only in <repo>
  -a, --architecture=<arch>   Search only in <arch>
  -j, --json                  Print the raw json
  -h, --help                  Show this screen
  -c, --config=<config>       Path to the config [default: /etc/kittypack.conf]
"""

import requests
import sys
import docopt
import yaml
import collections
from urllib.parse import urlencode


def search_db(pkg, **args):
    params = {"name": pkg}
    if "repo" in args:
        params["repo"] = args["repo"]
    if "arch" in args:
        params["arch"] = args["arch"]

    url = config["search_url"].format(params=urlencode(params))
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        fields = ("parsed", "raw", "url")
        Package = collections.namedtuple("Package", fields)
        return Package(parsed=req.json(), raw=req.text, url=url)
    else:
        req.raise_for_status()


def format_output(pkg, args):
    out = ("{repo}/{arch}/{pkgname}  {epoch}:{pkgver}-{pkgrel}\n"
           "  Updated: {last_update}  Built: {build_date}")
    return out.format(**pkg)


def read_config(path=None):
    path = "/etc/kittypack.conf" if path is None else path
    with open(path, "r") as fd:
        config = yaml.safe_load(fd)
    return config


def sort_by_repo(pkgs, conf):
    sortkey = lambda pkg: conf["repos"][pkg["repo"]]["s_idx"]
    return sorted(pkgs, key=sortkey)


if __name__ == "__main__":
    args = docopt.docopt(__doc__)  # will sys.exit(1) if invalid usage
    try:
        config = read_config(args["--config"])
    except OSError as e:
        print("Could not read the configuration file:\n  {}".format(e),
              file=sys.stderr)
        sys.exit(3)

    params = {}
    if args["--repository"]:
        try:
            params["repo"] = config["repos"][args["--repository".lower()]]["r_name"]
        except KeyError:
            print("error: Not a valid repository", file=sys.stderr)
            sys.exit(1)

    if args["--architecture"]:
        if args["--architecture"] in config["archs"]:
            params["arch"] = args["--architecture"]
        else:
            print("error: Not a valid architecture", file=sys.stderr)
            sys.exit(1)

    try:
        resp = search_db(args["<pkg>"], **params)
    except requests.exceptions.HTTPError as e:
        print("Error recieved from remote:", file=sys.stderr)
        print(e.args)
        sys.exit(4)

    if resp.parsed["valid"]:
        if args["--json"]:
            print(resp.raw)
        else:
            if not resp.parsed["results"]:
                print("No results found", file=sys.stderr)
                sys.exit(1)
            pkgs = sort_by_repo(resp.parsed["results"], config)
            print("\n\n".join(format_output(pkg, args) for pkg in pkgs))
    else:
        err = ("Hmm, archlinux.org didn't like my search.\n"
               "Url poked:  {}\n"
               "Json returned:  {}")
        print(err.format(resp.url, resp.raw), file=sys.stderr)
        sys.exit(4)
