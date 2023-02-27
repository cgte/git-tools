#!/usr/bin/python

"""
This module aims to automatically rebase unmerged branch onto target branch.
Goals:
        Nicer commit tree
        Save your time

"""


import sys, shlex
from subprocess import CalledProcessError
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
parser.add_argument(
    "--branch", "-b", default=None, help="specify only one branch to rebase"
)


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
    if params["branch"] is None:
        params["branch"] = current_branch()
    autorebase(**params)


@goback
def autorebase(target_branch, branch, **kwargs):
    if "sync_target" in kwargs:
        raise DeprecationWarning("Sync target is depreciated")
    diverged = unmerged(branch=target_branch)
    log.info("Diverged \n %r" % list(diverged))  # This should be displayed
    broader = broader_than(branch=target_branch)
    log.info("Broader \n %r" % list(broader))  # This shou;d be displayed too

    to_rebase = (
        diverged - broader
        if not branch
        else [
            branch,
        ]
    )
    to_rebase = [branch for branch in to_rebase if not shouldnot_rebase_branch(branch)]

    log.warn("branches to be rebased: %s", " ,".join(to_rebase))

    failed, success = [], []
    sys.stdout.flush()
    for branch in to_rebase:
        log.warn("rebasing %s", branch)
        try:
            get_lines(f"git rebase {target_branch}  {branch}")
            success.append(branch)
        except CalledProcessError:
            check_call(["git rebase --abort"], shell=True)
            failed.append(branch)

    return {"failed": failed, "succeeded": success}
