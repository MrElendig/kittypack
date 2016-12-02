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
  -f, --format=<fstring>      Use custom format string
  -j, --json                  Print the raw json
  -c, --config=<config>       Path to the config [default: /etc/kittypack.conf]
  -h, --help                  Show this screen
"""

import requests
import sys
import docopt
import yaml
import collections
from kittypack import fmt


def query_remote(url, params):
    """ Queries remote db and parses the return
    :params url: fully qualified url to remote
    :params params: parameters to give to the remote
    :type params: dict
    :returns namedtuple: (parsed=dict, raw=string, url=string)
    """
    req = requests.get(url, params=params)
    if req.status_code == requests.codes.ok:
        fields = ("parsed", "raw", "url")
        Package = collections.namedtuple("Package", fields)
        return Package(parsed=req.json(), raw=req.text, url=req.url)
    else:
        req.raise_for_status()



def read_config(path):
    with open(path, "r") as fd:
        config = yaml.safe_load(fd)
    return config


def sort_by_repo(pkgs, conf):
    """ Sorts packages based on the repo sort index
    :param pkgs: packages to be sorted
    :type pkgs: any iterable
    :param conf: configuration mapping
    :returns list: sorted list of packages
    """
    sortkey = lambda pkg: conf["repos"][pkg["repo"]]["s_idx"]
    return sorted(pkgs, key=sortkey)


def main():
    args = docopt.docopt(__doc__)  # will sys.exit(1) if invalid usage

    if args["--config"]:
        config_path = args["--config"]
    else:
        config_path = "/etc/kittypack.conf"
    try:
        config = read_config(config_path)
    except OSError as e:
        print("Could not read the configuration file:\n  {}".format(e),
              file=sys.stderr)
        sys.exit(3)

    params = {}
    params['name'] = args["<pkg>"]
    if args["--repository"]:
        try:
            repo = args["--repository".lower()]
            params["repo"] = config["repos"][repo]["r_name"]
        except KeyError:
            error_text = "error: {repo} is not a valid repository".format(
                repo=args["--repository"])
            print(error_text, file=sys.stderr)
            sys.exit(1)

    if args["--architecture"]:
        if args["--architecture"] in config["archs"]:
            params["arch"] = args["--architecture"]
        else:
            error_text = "error: {arch} is not a valid architecture".format(
                arch=args["--architecture"])
            print(error_text, file=sys.stderr)
            sys.exit(1)

    try:
        resp = query_remote(config["search_url"], params)
    except requests.exceptions.HTTPError as e:
        print("Error recieved from remote:", file=sys.stderr)
        print(e.args)
        sys.exit(4)

    if not resp.parsed["valid"]:
        err = ("Hmm, archlinux.org didn't like my search.\n"
               "Url poked:  {}\n"
               "Json returned:  {}")
        print(err.format(resp.url, resp.raw), file=sys.stderr)
        sys.exit(4)

    if args["--json"]:
        print(resp.raw)
    else:
        if not resp.parsed["results"]:
            print("No results found", file=sys.stderr)
            sys.exit(1)
        pkgs = sort_by_repo(resp.parsed["results"], config)
        if args["--format"]:
            print("\n".join(fmt.format_output(args["--format"], pkg) for pkg in pkgs))
        else:
            print("\n\n".join(fmt.template_output(pkg) for pkg in pkgs))
