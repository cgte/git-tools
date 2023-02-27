#!/usr/bin/python


import sys, shlex
from subprocess import CalledProcessError, check_output
from .commands import get_lines

from .gitcmd import sync_branch, unmerged, broader_than, goback

import argparse

import logging as log

from .utils import silent, devnull

default_rebase_onto_branch = "main"


parser = argparse.ArgumentParser("Automatic rebaser")
parser.add_argument(
    "--target-branch",
    "-t",
    default=f"{default_rebase_onto_branch}",
    help="name of the branch to rebase onto",
)

one_week = "1 week ago"

yesterday = "yesterday"


def current_branch():
    return get_lines("git rev-parse --abbrev-ref HEAD")[0]


def shouldnot_rebase_branch(branch_name):
    """
    >>> shouldnot_rebase_branch('valuable_research_norebase')
    False
    """
    return "norebase" in branch_name


def main(params=""):
    params = (
        vars(parser.parse_args(shlex.split(params)))
        if params
        else vars(parser.parse_args())
    )
    diagnose(**params)


@goback
def diagnose(target_branch, **kwargs):

    base_commit = f"git log --until='{one_week}'  -n 1 --oneline {target_branch}"
    base_hash = check_output(base_commit, shell=True, text=True).strip().split()[0]

    get_old_branches = (
        f"git branch -a --no-merged {base_hash} --no-contains {base_hash}"
    )
    # Branches qui sont en l'air  depuis longtemps

    """
    [cgoutte@e490 smpv2]$ git tip --oneline
82505da (HEAD -> companysum, origin/companysum) Check this branch
    La on peut supprimer les deux

    [cgoutte@e490 smpv2]$ git tip --oneline
    03f0b3a (HEAD -> build_tools, origin/fix_save_ruling_law_country) [CHG] First shot of csv implementation
    ici aussi mais pas de contrepartie distante
    """

    breakpoint()
