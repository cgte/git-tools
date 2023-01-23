#!/usr/bin/python

"""
This module aims to automatically rebase unmerged branch onto target branch.
Goals:
        Nicer commit tree
        Save your time

"""

import sys, shlex
from subprocess import check_call, CalledProcessError

from .gitcmd import unmerged, broader_than, goback, branches

import argparse

import logging as log

from .autorebase import autorebase


parser = argparse.ArgumentParser(
    "Checks your features branches "
    "are up to date with remote conuterparts "
    "then try to rebase/push them"
)

parser.add_argument(
    "--target-branch", "-t", default="master", help="name of the branch to rebase onto"
)
parser.add_argument(
    "--branch", "-b", default=None, help="specify only one branch to rebase"
)


def main(params=""):

    from pprint import pprint

    params = (
        vars(parser.parse_args(shlex.split(params)))
        if params
        else vars(parser.parse_args())
    )

    sync_features(**params)


def contains_remote_counterpart(branch, remote="origin"):
    return branch in broader_than("{remote}/{branch}".format(**locals()))


@goback
def sync_features(target_branch, branch, remote="origin", **kwargs):

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

    remote_branches = set(branches(origin=True))

    noremote = set()

    for branch in to_rebase:
        # This has no test.
        if branch not in remote_branches:
            print("%s is not on remote, not pulling" % branch)
            print("exectute the folowing for pushing")
            print("git push -u origin %s" % branch)
            noremote.add(branch)

    to_rebase = [
        branch
        for branch in to_rebase
        if branch not in noremote and contains_remote_counterpart(branch, remote)
    ]

    log.warn("branches to be updated: %s", " ,".join(to_rebase))

    failed, success = [], []

    for branch in to_rebase:
        result = autorebase(target_branch, branch)
        if result["succeeded"] and branch in result["succeeded"]:
            try:
                log.warn("pushing -f %s", branch)
                check_call(["git push -f %s %s" % (remote, branch)], shell=True)
                success.append(branch)
            except CalledProcessError:
                failed.append(branch)

    return {"failed": failed, "succeeded": success}
