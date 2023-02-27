#!/usr/bin/python

import shlex
from subprocess import CalledProcessError, check_call
from .commands import get_lines
from .utils import silent

from .gitcmd import goback

import argparse


default_rebase_onto_branch = "main"


parser = argparse.ArgumentParser("Automatic clean")


def current_branch():
    return get_lines("git rev-parse --abbrev-ref HEAD")[0]


def main(params=""):
    params = (
        vars(parser.parse_args(shlex.split(params)))
        if params
        else vars(parser.parse_args())
    )
    autoclean(**params)


def has_diff(reference):
    out = get_lines(f"git diff  {reference} ")
    filterd = [x.strip() for x in out]
    filterd = [x for x in filterd if x]
    return filterd


def remote_counterpart(branch, remote="origin"):
    return get_lines(f"git ls-remote --exit-code --heads {remote} {branch}")


@goback
def autoclean(target_branch=default_rebase_onto_branch):

    not_merged_local = get_lines(
        f"git branch --no-merged  {target_branch} |  sed 's/^*//' "
    )

    failed = []
    out_of_sync = []

    diverged = []

    to_delete_local = []
    to_delete_remote = []

    for branch in not_merged_local:
        get_lines("git checkout {branch}")
        remotes = remote_counterpart(branch)

        if remotes:
            for remote in remotes:
                hash_, name = remote.split()

                if get_lines(f"git diff {hash_}"):
                    print(f"{branch} is out of sync")
                    out_of_sync.append(branch)
                    continue

        try:
            command = f"git rebase {target_branch}  {branch}"
            check_call(command, shell=True)
        except CalledProcessError:
            check_call("git rebase --abort", shell=True, **silent)
            failed.append(branch)
            continue

        if has_diff(target_branch):
            diverged.append(branch)

        else:
            if remotes:
                to_delete_remote.append(branch)
            to_delete_local.append(branch)
    for b in to_delete_local:
        print(f"git branch -D {b}")
    for b in to_delete_remote:
        print(f"git push origin :{b}")
