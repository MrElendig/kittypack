#!/usr/bin/env python3

# kittypack: Grabs package info off archlinux.org/packages
# Copyright (C) 2019  Øyvind 'Mr.Elendig' Heggstad

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
import click
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
    req = requests.get(url, params=params, timeout=10)
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


@click.command()
@click.option('--repository', '-r', help='Search only in <repo>', metavar='<repo>')
@click.option('--architecture', '-a', help='Search only in <arch>', metavar='<arch>')
@click.option('--format', '-f', help='Use custom format string', metavar='<format>')
@click.option('--json', '-j', is_flag=True, help='Print the raw json')
@click.option('--config', '-c', type=click.Path(), default='/etc/kittypack.conf',
    show_default=True, help="Path to the config", metavar='<path>')
@click.argument('package')
def main(repository, architecture, format, json, config, package):
    """kittypack: A tool to grab basic package info from archlinux.org/packages"""
    try:
        config = read_config(config)
    except OSError as e:
        print("Could not read the configuration file:\n  {}".format(e),
              file=sys.stderr)
        sys.exit(3)

    params = {}
    params['name'] = package
    if repository:
        try:
            repo = repository.lower()
            params["repo"] = config["repos"][repo]["r_name"]
        except KeyError:
            error_text = "error: {repo} is not a valid repository".format(
                repo=repository)
            print(error_text, file=sys.stderr)
            sys.exit(1)

    if architecture:
        if architecture in config["archs"]:
            params["arch"] = architecture
        else:
            error_text = "error: {arch} is not a valid architecture".format(
                arch=architecture)
            print(error_text, file=sys.stderr)
            sys.exit(1)

    try:
        resp = query_remote(config["search_url"], params)
    except requests.exceptions.HTTPError as e:
        print("Error recieved from remote:", file=sys.stderr)
        print(e.args)
        sys.exit(4)
    except requests.exceptions.Timeout as e:
        print("Timed out connecting to the server")
        print(e)
        sys.exit(5)

    if not resp.parsed["valid"]:
        err = ("Hmm, archlinux.org didn't like my search.\n"
               "Url poked:  {}\n"
               "Json returned:  {}")
        print(err.format(resp.url, resp.raw), file=sys.stderr)
        sys.exit(4)

    if json:
        print(resp.raw)
    else:
        if not resp.parsed["results"]:
            print("No results found", file=sys.stderr)
            sys.exit(1)
        pkgs = sort_by_repo(resp.parsed["results"], config)
        if format:
            click.echo("\n".join(fmt.format_output(format, pkg) for pkg in pkgs))
        else:
            click.echo("\n\n".join(fmt.template_output(pkg) for pkg in pkgs))
